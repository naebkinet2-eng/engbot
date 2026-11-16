import json
import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL", "")
_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            raise RuntimeError("Не задана переменная окружения DATABASE_URL!")
        dsn = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        _pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)
    return _pool


async def close_db() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


async def init_db() -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                level TEXT DEFAULT NULL,
                audition_score INTEGER DEFAULT 0,
                audition_feedback TEXT DEFAULT '',
                best_interview_score INTEGER DEFAULT 0,
                last_interview_verdict TEXT DEFAULT '',
                lessons_completed TEXT DEFAULT '[]',
                words_practiced INTEGER DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)


async def get_or_create_user(user_id: int, username: str = "", full_name: str = "") -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
        if row is None:
            await conn.execute(
                "INSERT INTO users (user_id, username, full_name) VALUES ($1, $2, $3)",
                user_id,
                username or "",
                full_name or f"User {user_id}",
            )
            row = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
        else:
            if (username and row["username"] != username) or (full_name and row["full_name"] != full_name):
                await conn.execute(
                    "UPDATE users SET username = $1, full_name = $2 WHERE user_id = $3",
                    username or row["username"],
                    full_name or row["full_name"],
                    user_id,
                )
                row = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

        data = dict(row)
        data["lessons_completed"] = json.loads(data["lessons_completed"] or "[]")
        return data


async def save_audition_result(user_id: int, level: str, score: int, feedback: str) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE users
            SET level = $1, audition_score = $2, audition_feedback = $3
            WHERE user_id = $4
            """,
            level,
            score,
            feedback,
            user_id,
        )


async def complete_lesson(user_id: int, module_id: str, new_words: int = 8) -> dict:
    user = await get_or_create_user(user_id)
    completed = set(user["lessons_completed"])
    completed.add(module_id)
    updated_words = user["words_practiced"] + new_words

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE users
            SET lessons_completed = $1, words_practiced = $2
            WHERE user_id = $3
            """,
            json.dumps(list(completed)),
            updated_words,
            user_id,
        )
    return await get_or_create_user(user_id)


async def save_interview_result(user_id: int, score: int, verdict: str) -> dict:
    user = await get_or_create_user(user_id)
    best = max(user["best_interview_score"], score)

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE users
            SET best_interview_score = $1, last_interview_verdict = $2
            WHERE user_id = $3
            """,
            best,
            verdict,
            user_id,
        )
    return await get_or_create_user(user_id)


async def get_leaderboard() -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT user_id, username, full_name, level, best_interview_score,
                   last_interview_verdict, lessons_completed, words_practiced
            FROM users
            ORDER BY best_interview_score DESC, words_practiced DESC
            LIMIT 20
        """)
        result = []
        for r in rows:
            item = dict(r)
            item["lessons_count"] = len(json.loads(item["lessons_completed"] or "[]"))
            del item["lessons_completed"]
            result.append(item)
        return result
