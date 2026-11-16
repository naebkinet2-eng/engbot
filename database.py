import json
import aiosqlite

DB_PATH = "bot_data.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                level TEXT DEFAULT NULL,
                audition_score INTEGER DEFAULT 0,
                audition_feedback TEXT DEFAULT '',
                best_interview_score INTEGER DEFAULT 0,
                last_interview_verdict TEXT DEFAULT '',
                lessons_completed TEXT DEFAULT '[]',
                words_practiced INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def get_or_create_user(user_id: int, username: str = "", full_name: str = "") -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row is None:
            await db.execute(
                "INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
                (user_id, username or "", full_name or f"User {user_id}"),
            )
            await db.commit()
            cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
        else:
            if (username and row["username"] != username) or (full_name and row["full_name"] != full_name):
                await db.execute(
                    "UPDATE users SET username = ?, full_name = ? WHERE user_id = ?",
                    (username or row["username"], full_name or row["full_name"], user_id),
                )
                await db.commit()
                cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = await cursor.fetchone()

        data = dict(row)
        data["lessons_completed"] = json.loads(data["lessons_completed"] or "[]")
        return data


async def save_audition_result(user_id: int, level: str, score: int, feedback: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            UPDATE users
            SET level = ?, audition_score = ?, audition_feedback = ?
            WHERE user_id = ?
            """,
            (level, score, feedback, user_id),
        )
        await db.commit()


async def complete_lesson(user_id: int, module_id: str, new_words: int = 8) -> dict:
    user = await get_or_create_user(user_id)
    completed = set(user["lessons_completed"])
    completed.add(module_id)
    updated_words = user["words_practiced"] + new_words

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            UPDATE users
            SET lessons_completed = ?, words_practiced = ?
            WHERE user_id = ?
            """,
            (json.dumps(list(completed)), updated_words, user_id),
        )
        await db.commit()
    return await get_or_create_user(user_id)


async def save_interview_result(user_id: int, score: int, verdict: str) -> dict:
    user = await get_or_create_user(user_id)
    best = max(user["best_interview_score"], score)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            UPDATE users
            SET best_interview_score = ?, last_interview_verdict = ?
            WHERE user_id = ?
            """,
            (best, verdict, user_id),
        )
        await db.commit()
    return await get_or_create_user(user_id)


async def get_leaderboard() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT user_id, username, full_name, level, best_interview_score,
                   last_interview_verdict, lessons_completed, words_practiced
            FROM users
            ORDER BY best_interview_score DESC, words_practiced DESC
            LIMIT 20
        """)
        rows = await cursor.fetchall()
        result = []
        for r in rows:
            item = dict(r)
            item["lessons_count"] = len(json.loads(item["lessons_completed"] or "[]"))
            del item["lessons_completed"]
            result.append(item)
        return result
