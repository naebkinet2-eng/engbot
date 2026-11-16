import asyncio
import json
import os
import re
import httpx
from google import genai
from google.genai import types
import curriculum

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GROQ_TEXT_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
GEMINI_MODELS = ["gemini-3.5-flash-lite", "gemini-3.6-flash", "gemini-3.8-flash"]

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


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


async def _transcribe_with_groq(audio_bytes: bytes, audio_mime: str = "audio/webm") -> str:
    if not GROQ_API_KEY or not audio_bytes:
        return ""
    clean_mime = _normalize_audio_mime(audio_mime)
    ext = "ogg" if "ogg" in clean_mime else ("mp4" if "mp4" in clean_mime else "webm")

    async with httpx.AsyncClient(timeout=20.0) as http:
        resp = await http.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            files={"file": (f"speech.{ext}", audio_bytes, clean_mime)},
            data={
                "model": "whisper-large-v3-turbo",
                "language": "en",
                "response_format": "json",
            },
        )
        resp.raise_for_status()
        return resp.json().get("text", "").strip()


async def _groq_json_completion(prompt: str, temperature: float = 0.3, timeout: float = 20.0) -> dict:
    last_err: Exception | None = None
    async with httpx.AsyncClient(timeout=timeout) as http:
        for model_name in GROQ_TEXT_MODELS:
            try:
                resp = await http.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a helpful English coach API. Always reply with strictly valid JSON matching the requested schema, with no markdown fences.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": temperature,
                        "response_format": {"type": "json_object"},
                    },
                )
                resp.raise_for_status()
                content = resp.json()["choices"][0]["message"]["content"]
                return _parse_json(content)
            except Exception as exc:
                last_err = exc
                print(f"[Groq] Model '{model_name}' failed: {str(exc)[:180]}")
    raise RuntimeError(f"Groq API error: {last_err}")


async def _gemini_json_completion(contents: list, temperature: float = 0.3, timeout: float = 18.0) -> dict:
    if not gemini_client:
        raise RuntimeError("GEMINI_API_KEY не настроен")

    last_err: Exception | None = None
    for model_name in GEMINI_MODELS:
        try:
            response = await asyncio.wait_for(
                gemini_client.aio.models.generate_content(
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
            last_err = exc
            print(f"[Gemini] Model '{model_name}' failed: {str(exc)[:180]}")
            await asyncio.sleep(0.5)
    raise RuntimeError(f"Gemini API error: {last_err}")


async def _generate_json_smart(
    prompt: str,
    audio_parts: list[tuple[str, bytes, str]] | None = None,
    temperature: float = 0.3,
    timeout: float = 22.0,
) -> dict:
    """
    1. Если задан GROQ_API_KEY — транскрибирует аудио через Whisper Large V3 Turbo
       и генерирует JSON через Groq (gpt-oss-120b / gpt-oss-20b).
    2. Если Groq не настроен или недоступен — автоматически идет в Gemini (3.5-flash-lite / 3.6-flash / 3.8-flash).
    """
    if not GROQ_API_KEY and not gemini_client:
        raise RuntimeError("Добавьте GROQ_API_KEY или GEMINI_API_KEY в настройки Render.")

    if GROQ_API_KEY:
        try:
            enriched_prompt = prompt
            if audio_parts:
                transcripts = []
                for label, raw_bytes, mime in audio_parts:
                    text = await _transcribe_with_groq(raw_bytes, mime)
                    transcripts.append(f"- {label} (распознано Whisper с микрофона): \"{text or '[неразборчиво / тишина]'}\"")
                enriched_prompt += "\n\nРаспознанная речь пользователя с микрофона:\n" + "\n".join(transcripts)

            return await _groq_json_completion(enriched_prompt, temperature=temperature, timeout=timeout)
        except Exception as groq_exc:
            print(f"[AI Router] Groq fallback to Gemini: {groq_exc}")
            if not gemini_client:
                raise RuntimeError("Ошибка Groq API. Попробуйте повторить отправку через пару секунд.") from groq_exc

    contents: list = [prompt]
    if audio_parts:
        for label, raw_bytes, mime in audio_parts:
            contents.append(f"{label}:")
            contents.append(types.Part.from_bytes(data=raw_bytes, mime_type=_normalize_audio_mime(mime)))

    try:
        return await _gemini_json_completion(contents, temperature=temperature, timeout=timeout)
    except Exception as gem_exc:
        raise RuntimeError(
            "ИИ-сервис временно перегружен. Ваши ответы сохранены — нажмите кнопку отправки ещё раз через 5 секунд."
        ) from gem_exc


async def evaluate_audition(
    quiz_score: int,
    text_answer: str = "",
    audio_bytes: bytes | None = None,
    audio_mime: str = "audio/webm",
) -> dict:
    prompt = f"""
    Ты строгий, но дружелюбный преподаватель английского для кандидатов на рабочую визу США H-2B / H-2A (рыбзавод, сезонная работа).
    Кандидат прошел входной Audition:
    - Баллы за базовый тест (из 3): {quiz_score}
    - Текстовый ответ кандидата (если был): "{text_answer}"
    - Вопрос голосовой визитки: "Introduce yourself in English and explain why you want to work in the United States this season."

    Оцени уровень английского кандидата (грамматика, словарный запас, четкость речи).
    Присвой один из трех грейдов:
    - "Novice" (A1-A2: базовые знания, много ошибок)
    - "Worker" (B1: уверенный разговорный для цеха, понятная речь с небольшими ошибками)
    - "Pro" (B2+: свободная речь, отличный словарный запас, готов к сложным вопросам консула)

    Верни СТРОГО JSON:
    {{
      "level": "Novice" | "Worker" | "Pro",
      "score": число от 10 до 100,
      "transcript": "что сказал кандидат (текст или распознанное аудио)",
      "feedback": "разбор на русском языке (3-4 предложения: уровень, качество речи и на что сделать упор)"
    }}
    """

    audio_parts = [("Голосовая визитка кандидата", audio_bytes, audio_mime)] if audio_bytes else None
    return await _generate_json_smart(prompt, audio_parts=audio_parts, temperature=0.3)


async def evaluate_pronunciation(
    target_phrase: str,
    text_attempt: str = "",
    audio_bytes: bytes | None = None,
    audio_mime: str = "audio/webm",
) -> dict:
    prompt = f"""
    Ты тренер по американскому произношению и дикции для работы в США.
    Эталонная фраза: "{target_phrase}"
    Текстовая попытка (если без микрофона): "{text_attempt}"

    Сравни распознанную речь (или текст) с эталонной фразой:
    1. Все ли слова произнесены правильно и четко распознались?
    2. Поймет ли эту фразу американский супервайзер в шумном цеху?
    3. Какие звуки или слова стоит потренировать?

    Верни СТРОГО JSON:
    {{
      "score": число от 0 до 100,
      "transcript": "что именно произнес кандидат",
      "diction_tips": "конкретный разбор на русском: какие слова прозвучали отлично, а какие нужно поправить (с русской транскрипцией сложных слов)",
      "passed": true если score >= 60 иначе false
    }}
    """

    audio_parts = [("Запись произношения фразы", audio_bytes, audio_mime)] if audio_bytes else None
    return await _generate_json_smart(prompt, audio_parts=audio_parts, temperature=0.3)


async def generate_dynamic_lesson(level: str, topic: str) -> dict:
    prompt = f"""
    Сгенерируй мини-урок английского языка для подготовки к работе в США по визе H-2B / H-2A (рыбзавод, производство, быт в США).
    Уровень студента: {level} (Novice = простые фразы, Worker = рабочий разговорный, Pro = сложные ситуации и идиомы).
    Тема урока: "{topic}".

    ОБЯЗАТЕЛЬНО разбей каждую английскую реплику в диалоге на массив пар ["английское_слово_со_знаком_препинания", "точный_контекстный_перевод_на_русский"], чтобы пользователь мог нажать на ЛЮБОЕ слово и увидеть перевод.

    Верни СТРОГО JSON следующей структуры без вложенных оберток:
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

    raw = await _generate_json_smart(prompt, temperature=0.7)
    if isinstance(raw, dict) and "lesson" in raw and isinstance(raw["lesson"], dict):
        raw = raw["lesson"]

    dialogue = raw.get("dialogue") if isinstance(raw.get("dialogue"), list) else []
    normalized_dialogue = []
    for line in dialogue:
        if not isinstance(line, dict):
            continue
        speaker = str(line.get("speaker") or "Supervisor")
        tokens = line.get("tokens")
        if isinstance(tokens, list) and tokens:
            clean_tokens = [
                [str(t[0]), str(t[1])] if isinstance(t, (list, tuple)) and len(t) >= 2 else [str(t), ""]
                for t in tokens
            ]
        else:
            text = str(line.get("text") or line.get("en") or "Ready to work.")
            clean_tokens = [[w, ""] for w in text.split()]
        normalized_dialogue.append({"speaker": speaker, "tokens": clean_tokens})

    if not normalized_dialogue:
        normalized_dialogue = [
            {
                "speaker": "Supervisor",
                "tokens": [["Please", "Пожалуйста,"], ["check", "проверь"], ["the", "эту"], ["line.", "линию."]],
            },
            {
                "speaker": "You",
                "tokens": [["Got", "Понял"], ["it,", "вас,"], ["right", "прямо"], ["away.", "сейчас."]],
            },
        ]

    builder = raw.get("builder") if isinstance(raw.get("builder"), dict) else {}
    answer_str = str(builder.get("answer") or "I am ready to start my shift now.").strip()
    words_list = builder.get("words") if isinstance(builder.get("words"), list) and builder.get("words") else answer_str.split()

    return {
        "id": str(raw.get("id") or "ai_custom"),
        "title": str(raw.get("title") or f"Практика: {topic}"),
        "tag": str(raw.get("tag") or f"AI Practice ({level})"),
        "description": str(raw.get("description") or f"Ситуация: {topic}"),
        "dialogue": normalized_dialogue,
        "builder": {
            "ru": str(builder.get("ru") or "Я готов начать свою смену прямо сейчас."),
            "words": [str(w) for w in words_list],
            "answer": answer_str,
        },
        "speaking_prompt": str(raw.get("speaking_prompt") or answer_str),
    }


async def generate_random_interview(level: str = "Worker") -> list[dict]:
    base_questions = curriculum.get_random_interview_set()
    if not GROQ_API_KEY and not gemini_client:
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
        data = await _generate_json_smart(prompt, temperature=0.8, timeout=10.0)
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
    - 9 000 – 10 000: Идеальное прохождение (уверенная речь, четкий английский, никаких визовых red flags, полная готовность к тяжелой работе).
    - 7 000 – 8 999: Хороший уровень (виза и работа скорее всего одобрены, есть мелкие ошибки в грамматике).
    - 4 500 – 6 999: На грани (слабый словарный запас, неуверенные ответы, требуется доработка).
    - 0 – 4 499: Отказ (непонимание вопросов, подозрение на иммиграционные намерения или незнание техники безопасности).

    ВАЖНО: Кандидат ответил голосом на {voice_count} из 6 вопросов. Максимально возможный балл для этой сессии ограничен {max_cap}.

    Список вопросов и ответов:
    {json.dumps(answers_payload, ensure_ascii=False, indent=2)}

    Верни СТРОГО JSON:
    {{
      "total_score": целое число от 0 до {max_cap},
      "verdict": "APPROVED (Виза и оффер одобрены)" | "BORDERLINE (Высокий риск отказа)" | "REFUSED (Отказ)",
      "diction_score": число от 0 до 100,
      "grammar_score": число от 0 до 100,
      "visa_safety_score": число от 0 до 100,
      "summary": "Общий вердикт на русском (3-4 предложения: впечатление консула и работодателя).",
      "breakdown": [
        {{
          "question_num": 1,
          "what_you_said": "Кратко что ответил кандидат",
          "critique": "Разбор ошибок (грамматика, точность речи, смысл) на русском",
          "ideal_answer": "Пример идеального естественного ответа на английском"
        }}
      ]
    }}
    """

    audio_parts: list[tuple[str, bytes, str]] = []
    for idx, item in enumerate(answers_payload, start=1):
        qid = item["id"]
        if qid in audio_files:
            raw_bytes, mime = audio_files[qid]
            audio_parts.append((f"Аудиоответ на вопрос #{idx} ({qid})", raw_bytes, mime))

    return await _generate_json_smart(prompt, audio_parts=audio_parts or None, temperature=0.3, timeout=28.0)
