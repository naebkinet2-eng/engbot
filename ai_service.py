import json
import os
import re
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _parse_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


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
        clean_mime = audio_mime.split(";")[0] if audio_mime else "audio/webm"
        contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=clean_mime))

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )
    return _parse_json(response.text)


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
        clean_mime = audio_mime.split(";")[0] if audio_mime else "audio/webm"
        contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=clean_mime))

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )
    return _parse_json(response.text)


async def generate_dynamic_lesson(level: str, topic: str) -> dict:
    if not client:
        raise RuntimeError("GEMINI_API_KEY не настроен в .env")

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

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    return _parse_json(response.text)


async def evaluate_full_interview(answers_payload: list[dict], audio_files: dict[str, tuple[bytes, str]]) -> dict:
    """
    answers_payload: [{"id": "int_1", "role": "...", "question": "...", "text": "...", "has_audio": bool}, ...]
    audio_files: {"int_1": (bytes, mime_type), ...}
    """
    if not client:
        return {
            "total_score": 5000,
            "verdict": "DEMO MODE",
            "diction_score": 50,
            "grammar_score": 50,
            "visa_safety_score": 50,
            "summary": "Укажите GEMINI_API_KEY в .env для реальной оценки собеседования.",
            "breakdown": []
        }

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
            clean_mime = mime.split(";")[0] if mime else "audio/webm"
            contents.append(f"Аудиоответ на вопрос {qid}:")
            contents.append(types.Part.from_bytes(data=raw_bytes, mime_type=clean_mime))

    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3,
        ),
    )
    return _parse_json(response.text)
