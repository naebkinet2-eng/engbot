import asyncio
import json
import os
import re
from google import genai
from google.genai import types
import curriculum

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

FALLBACK_MODELS = list(dict.fromkeys([
    PRIMARY_MODEL,
    "gemini-3.8-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
]))

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _parse_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _normalize_audio_mime(mime: str | None) -> str:
    if not mime:
        return "audio/webm"
    base = mime.split(";")[0].strip().lower()
    if not base.startswith("audio/"):
        return "audio/webm"
    return base


async def _generate_json_with_fallback(contents: list, temperature: float = 0.3, timeout: float = 22.0) -> dict:
    if not client:
        raise RuntimeError("GEMINI_API_KEY не настроен в переменных окружения Render")

    last_error: Exception | None = None
    for idx, model_name in enumerate(FALLBACK_MODELS):
        try:
            response = await asyncio.wait_for(
                client.aio.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=temperature,
                    ),
                ),
                timeout=timeout,
            )
            return _parse_json(response.text)
        except Exception as exc:
            last_error = exc
            err_str = str(exc)
            print(f"[Gemini Fallback] Model '{model_name}' failed: {err_str[:180]}")
            # Если модель перегружена (503), исчерпан лимит (429), не найдена (404) или таймаут — пробуем следующую
            if idx < len(FALLBACK_MODELS) - 1:
                await asyncio.sleep(0.8)
                continue

    raise RuntimeError(
        f"Серверы Google Gemini временно перегружены (503). Ваши ответы сохранены — нажмите кнопку отправки еще раз через пару секунд. ({last_error})"
    )


async def evaluate_audition(
    quiz_score: int,
    text_answer: str = "",
    audio_bytes: bytes | None = None,
    audio_mime: str = "audio/webm",
) -> dict:
    if not client:
        level = "Worker" if quiz_score >= 2 else "Novice"
        return {
            "level": level,
            "score": quiz_score * 30,
            "feedback": "GEMINI_API_KEY не задан, уровень определен по базовому тесту."
        }

    prompt = f"""
    Ты строгий, но дружелюбный преподаватель английского для кандидатов на рабочую визу США H-2B / H-2A (рыбзавод, сезонная работа).
    Кандидат прошел входной Audition:
    - Баллы за базовый тест (из 3): {quiz_score}
    - Текстовый ответ кандидата (если был): "{text_answer}"
    - Также прикреплено голосовое сообщение (если кандидат записал голос) с ответом на вопрос:
      "Introduce yourself in English and explain why you want to work in the United States this season."

    Оцени уровень английского кандидата (грамматика, словарный запас, и если есть аудио — дикцию и четкость произношения).
    Присвой один из трех грейдов:
    - "Novice" (A1-A2: базовые знания, сильный акцент или много ошибок)
    - "Worker" (B1: уверенный разговорный для цеха, понятная речь с небольшими ошибками)
    - "Pro" (B2+: свободная речь, хорошая дикция, готов к сложным вопросам консула)

    Верни СТРОГО JSON без markdown:
    {{
      "level": "Novice" | "Worker" | "Pro",
      "score": число от 10 до 100,
      "transcript": "что ты услышал от кандидата (или его текст)",
      "feedback": "разбор на русском языке (3-4 предложения: уровень, оценка дикции/произношения, на что сделать упор)"
    }}
    """

    contents: list = [prompt]
    if audio_bytes:
        clean_mime = _normalize_audio_mime(audio_mime)
        contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=clean_mime))

    return await _generate_json_with_fallback(contents, temperature=0.3)


async def evaluate_pronunciation(
    target_phrase: str,
    text_attempt: str = "",
    audio_bytes: bytes | None = None,
    audio_mime: str = "audio/webm",
) -> dict:
    if not client:
        return {
            "score": 80,
            "transcript": text_attempt or target_phrase,
            "diction_tips": "Добавьте GEMINI_API_KEY для детального анализа произношения.",
            "passed": True
        }

    prompt = f"""
    Ты тренер по американскому произношению и дикции для работы в США.
    Эталонная фраза: "{target_phrase}"
    Текстовая попытка (если без микрофона): "{text_attempt}"

    Если приложено аудио — внимательно послушай, как кандидат произнес фразу:
    1. Насколько четко звучат согласные и гласные (дикция)?
    2. Правильно ли поставлены ударения и интонация?
    3. Поймет ли его американский супервайзер в шумном цеху?

    Верни СТРОГО JSON:
    {{
      "score": число от 0 до 100,
      "transcript": "что именно произнес кандидат",
      "diction_tips": "конкретный разбор на русском: какие слова/звуки прозвучали отлично, а какие нужно поправить (с русской транскрипцией сложных звуков)",
      "passed": true если score >= 60 иначе false
    }}
    """

    contents: list = [prompt]
    if audio_bytes:
        clean_mime = _normalize_audio_mime(audio_mime)
        contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=clean_mime))

    return await _generate_json_with_fallback(contents, temperature=0.3)


async def generate_dynamic_lesson(level: str, topic: str) -> dict:
    prompt = f"""
    Сгенерируй мини-урок английского языка для подготовки к работе в США по визе H-2B / H-2A (рыбзавод, производство, быт в США).
    Уровень студента: {level} (Novice = простые фразы, Worker = рабочий разговорный, Pro = сложные ситуации и идиомы).
    Тема урока: "{topic}".

    ОБЯЗАТЕЛЬНО разбей каждую английскую реплику в диалоге на массив пар ["английское_слово_со_знаком_препинания", "точный_контекстный_перевод_на_русский"], чтобы пользователь мог нажать на ЛЮБОЕ слово и увидеть перевод.

    Верни СТРОГО JSON следующей структуры:
    {{
      "id": "ai_custom",
      "title": "Короткое название урока на русском",
      "tag": "AI Practice ({level})",
      "description": "Краткое описание ситуации (1 предложение)",
      "dialogue": [
        {{
          "speaker": "Supervisor",
          "tokens": [["English", "Английское"], ["word.", "слово."]]
        }},
        {{
          "speaker": "You",
          "tokens": [["Understood,", "Понял,"], ["boss.", "босс."]]
        }},
        {{
          "speaker": "Supervisor",
          "tokens": [["Good", "Отличная"], ["job.", "работа."]]
        }}
      ],
      "builder": {{
        "ru": "Перевод предложения на русский для сборки",
        "words": ["Массив", "английских", "слов", "в", "правильном", "порядке."],
        "answer": "Правильное английское предложение целиком."
      }},
      "speaking_prompt": "Одна полезная рабочая фраза на английском для тренировки произношения вслух."
    }}
    """

    return await _generate_json_with_fallback([prompt], temperature=0.7)


async def generate_random_interview(level: str = "Worker") -> list[dict]:
    """
    Берет случайные 2+2 из богатого пула (24 вопроса с пословным переводом)
    и добавляет 1+1 уникальных свежих вопроса от AI (если Gemini доступен),
    либо возвращает 3+3 из пула при высокой нагрузке.
    """
    base_questions = curriculum.get_random_interview_set()
    if not client:
        return base_questions

    prompt = f"""
    Сгенерируй 2 уникальных вопроса для собеседования на сезонную работу в США (виза H-2B / рыбзавод) под уровень {level}:
    - 1 вопрос от лица "Consular Officer (Посольство США)"
    - 1 вопрос от лица "US Plant Supervisor (Работодатель, США)"

    Разбей каждый вопрос на массив пар tokens: [["English", "Русский"], ...] для пословного перевода при нажатии.
    Верни СТРОГО JSON:
    {{
      "questions": [
        {{
          "id": "ai_con_1",
          "role": "Consular Officer (Посольство США)",
          "question": "Полный вопрос на английском?",
          "tokens": [["Full", "Полный"], ["question?", "вопрос?"]],
          "hint_ru": "Краткая подсказка на русском как ответить правильно"
        }},
        {{
          "id": "ai_emp_1",
          "role": "US Plant Supervisor (Работодатель, США)",
          "question": "Полный рабочий вопрос на английском?",
          "tokens": [["Full", "Полный"], ["work", "рабочий"], ["question?", "вопрос?"]],
          "hint_ru": "Краткая подсказка на русском"
        }}
      ]
    }}
    """
    try:
        data = await _generate_json_with_fallback([prompt], temperature=0.8, timeout=10.0)
        ai_qs = data.get("questions", [])
        if len(ai_qs) == 2 and all("tokens" in q and "question" in q for q in ai_qs):
            return [base_questions[0], base_questions[1], ai_qs[0], base_questions[3], base_questions[4], ai_qs[1]]
    except Exception:
        pass

    return base_questions


async def evaluate_full_interview(answers_payload: list[dict], audio_files: dict[str, tuple[bytes, str]]) -> dict:
    voice_count = len(audio_files)
    max_cap = 10000 if voice_count >= 4 else (9000 if voice_count >= 1 else 8200)

    prompt = f"""
    Ты — экзаменационная комиссия, состоящая из Консульского офицера Посольства США (виза H-2B/H-2A) и Американского супервайзера рыбзавода (Аляска / побережье США).
    Кандидат прошел финальное собеседование из 6 вопросов (3 визовых + 3 рабочих).

    ШКАЛА ОЦЕНКИ: от 0 до 10 000 баллов!
    - 9 000 – 10 000: Идеальное прохождение (уверенная дикция, четкий английский, никаких визовых red flags, полная готовность к тяжелой работе).
    - 7 000 – 8 999: Хороший уровень (виза и работа скорее всего одобрены, есть мелкие ошибки в грамматике или акценте).
    - 4 500 – 6 999: На грани (слабый словарный запас, неуверенные ответы, требуется доработка).
    - 0 – 4 499: Отказ (непонимание вопросов, подозрение на иммиграционные намерения или незнание техники безопасности).

    ВАЖНО: Кандидат ответил голосом на {voice_count} из 6 вопросов. Максимально возможный балл для этой сессии ограничен {max_cap} (поскольку проверка дикции требует живого голоса).

    Список вопросов и текстовых ответов (аудиофайлы прикреплены в том же порядке для вопросов с has_audio=true):
    {json.dumps(answers_payload, ensure_ascii=False, indent=2)}

    Прослушай все прикрепленные аудиозаписи (оцени дикцию, произношение, скорость и уверенность речи) и проанализируй смысл каждого из 6 ответов.
    Верни СТРОГО JSON:
    {{
      "total_score": целое число от 0 до {max_cap},
      "verdict": "APPROVED (Виза и оффер одобрены)" | "BORDERLINE (Высокий риск отказа)" | "REFUSED (Отказ)",
      "diction_score": число от 0 до 100,
      "grammar_score": число от 0 до 100,
      "visa_safety_score": число от 0 до 100,
      "summary": "Общий вердикт на русском (3-4 предложения: как звучал кандидат, впечатление консула и работодателя).",
      "breakdown": [
        {{
          "question_num": 1,
          "what_you_said": "Кратко что сказал/произнес кандидат",
          "critique": "Разбор ошибок (грамматика, произношение, смысл) на русском",
          "ideal_answer": "Пример идеального естественного ответа на английском"
        }}
      ]
    }}
    """

    contents: list = [prompt]
    for item in answers_payload:
        qid = item["id"]
        if qid in audio_files:
            raw_bytes, mime = audio_files[qid]
            clean_mime = _normalize_audio_mime(mime)
            contents.append(f"Аудиоответ на вопрос {qid}:")
            contents.append(types.Part.from_bytes(data=raw_bytes, mime_type=clean_mime))

    return await _generate_json_with_fallback(contents, temperature=0.3, timeout=35.0)
