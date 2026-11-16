import asyncio
import hashlib
import hmac
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import parse_qsl

import uvicorn
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

import ai_service
import curriculum
import database

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "").rstrip("/")
PORT = int(os.getenv("PORT", "8000"))
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- Telegram Bot Handlers ---
@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    if user:
        await database.get_or_create_user(
            user_id=user.id,
            username=user.username or "",
            full_name=user.full_name or "",
        )

    if not WEBAPP_URL:
        await message.answer("⚠️ Ошибка конфигурации: не указан WEBAPP_URL в .env")
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇸 Открыть H-2B / Seafood English App",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )
    await message.answer(
        "Привет! Это ваш закрытый тренажер английского для работы в США (визы H-2B / H-2A, рыбзавод, граница и посольство).\n\n"
        "Внутри тебя ждет:\n"
        "1️⃣ **Audition** — входная проверка уровня и дикции\n"
        "2️⃣ **Интерактивный курс** — нажимай на любое слово для мгновенного перевода + тренировка произношения голосом\n"
        "3️⃣ **Собеседование 3+3 (до 10 000 баллов)** и общий рейтинг друзей\n\n"
        "Жми кнопку ниже, чтобы начать 👇",
        reply_markup=kb,
        parse_mode="Markdown",
    )


@dp.message(F.text == "/top")
async def cmd_top(message: Message) -> None:
    leaders = await database.get_leaderboard()
    if not leaders:
        await message.answer("Рейтинг пока пуст.")
        return

    lines = ["🏆 **Рейтинг кандидатов (макс. 10 000 баллов):**\n"]
    medals = ["🥇", "🥈", "🥉"]
    for idx, item in enumerate(leaders):
        prefix = medals[idx] if idx < 3 else f"{idx + 1}."
        lvl = item["level"] or "Без Audition"
        lines.append(
            f"{prefix} **{item['full_name']}** [{lvl}] — **{item['best_interview_score']}** баллов"
        )
    await message.answer("\n".join(lines), parse_mode="Markdown")


# --- Telegram Mini App Auth Verification ---
def verify_telegram_init_data(init_data: str) -> dict:
    if not init_data:
        if DEV_MODE:
            return {"id": 100001, "username": "dev_user", "first_name": "Dev Tester"}
        raise HTTPException(status_code=401, detail="Missing Telegram initData")

    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=401, detail="Invalid initData signature")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(status_code=401, detail="Telegram signature mismatch")

    user_json = parsed.get("user", "{}")
    return json.loads(user_json)


async def get_current_tg_user(x_telegram_init_data: str = Header(default="")) -> dict:
    tg_user = verify_telegram_init_data(x_telegram_init_data)
    full_name = " ".join(
        filter(None, [tg_user.get("first_name", ""), tg_user.get("last_name", "")])
    ).strip()
    return await database.get_or_create_user(
        user_id=int(tg_user["id"]),
        username=tg_user.get("username", ""),
        full_name=full_name or f"User {tg_user['id']}",
    )


# --- FastAPI Lifespan & Routes ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    if WEBAPP_URL and BOT_TOKEN:
        try:
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(
                    text="English H-2B",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            )
        except Exception as e:
            print(f"Menu button setup warning: {e}")

    polling_task = asyncio.create_task(dp.start_polling(bot))
    yield
    polling_task.cancel()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
async def serve_webapp():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/bootstrap")
async def api_bootstrap(x_telegram_init_data: str = Header(default="")):
    user = await get_current_tg_user(x_telegram_init_data)
    leaderboard = await database.get_leaderboard()
    return {
        "user": user,
        "audition_questions": curriculum.AUDITION_QUESTIONS,
        "modules": curriculum.MODULES,
        "interview_questions": curriculum.INTERVIEW_QUESTIONS,
        "leaderboard": leaderboard,
    }


@app.post("/api/audition")
async def api_submit_audition(
    quiz_score: int = Form(...),
    text_answer: str = Form(default=""),
    audio: UploadFile | None = File(default=None),
    x_telegram_init_data: str = Header(default=""),
):
    user = await get_current_tg_user(x_telegram_init_data)
    audio_bytes = await audio.read() if audio else None
    audio_mime = (audio.content_type or "audio/webm") if audio else "audio/webm"

    result = await ai_service.evaluate_audition(
        quiz_score=quiz_score,
        text_answer=text_answer,
        audio_bytes=audio_bytes,
        audio_mime=audio_mime,
    )
    level = result.get("level", "Worker")
    if level not in ("Novice", "Worker", "Pro"):
        level = "Worker"

    await database.save_audition_result(
        user_id=user["user_id"],
        level=level,
        score=int(result.get("score", 50)),
        feedback=result.get("feedback", ""),
    )
    updated_user = await database.get_or_create_user(user["user_id"])
    return {"result": result, "user": updated_user}


@app.post("/api/pronunciation")
async def api_check_pronunciation(
    target_phrase: str = Form(...),
    text_attempt: str = Form(default=""),
    audio: UploadFile | None = File(default=None),
    x_telegram_init_data: str = Header(default=""),
):
    await get_current_tg_user(x_telegram_init_data)
    audio_bytes = await audio.read() if audio else None
    audio_mime = (audio.content_type or "audio/webm") if audio else "audio/webm"

    result = await ai_service.evaluate_pronunciation(
        target_phrase=target_phrase,
        text_attempt=text_attempt,
        audio_bytes=audio_bytes,
        audio_mime=audio_mime,
    )
    return result


@app.post("/api/lesson/complete")
async def api_complete_lesson(
    module_id: str = Form(...),
    x_telegram_init_data: str = Header(default=""),
):
    user = await get_current_tg_user(x_telegram_init_data)
    updated_user = await database.complete_lesson(user["user_id"], module_id)
    leaderboard = await database.get_leaderboard()
    return {"user": updated_user, "leaderboard": leaderboard}


@app.post("/api/lesson/generate")
async def api_generate_lesson(
    topic: str = Form(default="Работа на линии заморозки и общение с бригадиром"),
    x_telegram_init_data: str = Header(default=""),
):
    user = await get_current_tg_user(x_telegram_init_data)
    level = user.get("level") or "Worker"
    lesson = await ai_service.generate_dynamic_lesson(level=level, topic=topic)
    return {"lesson": lesson}


@app.post("/api/interview/submit")
async def api_submit_interview(
    request: Request,
    x_telegram_init_data: str = Header(default=""),
):
    user = await get_current_tg_user(x_telegram_init_data)
    form = await request.form()

    answers_raw = form.get("answers_json", "[]")
    answers_payload = json.loads(str(answers_raw))

    audio_files: dict[str, tuple[bytes, str]] = {}
    for item in answers_payload:
        qid = item["id"]
        file_obj = form.get(f"audio_{qid}")
        if file_obj and hasattr(file_obj, "read"):
            raw_bytes = await file_obj.read()
            if raw_bytes:
                audio_files[qid] = (raw_bytes, getattr(file_obj, "content_type", "audio/webm") or "audio/webm")
                item["has_audio"] = True

    evaluation = await ai_service.evaluate_full_interview(answers_payload, audio_files)
    total_score = max(0, min(10000, int(evaluation.get("total_score", 0))))
    verdict = evaluation.get("verdict", "COMPLETED")

    updated_user = await database.save_interview_result(
        user_id=user["user_id"],
        score=total_score,
        verdict=verdict,
    )
    leaderboard = await database.get_leaderboard()
    return {
        "evaluation": evaluation,
        "user": updated_user,
        "leaderboard": leaderboard,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False)
