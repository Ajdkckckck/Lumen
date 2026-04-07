import sqlite3
from datetime import datetime

import pytz

from bot.config import DB_PATH, TIMEZONE

tz = pytz.timezone(TIMEZONE)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def now_local() -> datetime:
    return datetime.now(tz)


def now_str() -> str:
    return now_local().strftime("%Y-%m-%d %H:%M:%S")


def today_str() -> str:
    return now_local().strftime("%Y-%m-%d")


def init_db() -> None:
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS compliments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS schedule_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            text TEXT NOT NULL,
            hour INTEGER NOT NULL,
            minute INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS diary_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS letters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS support_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS time_capsules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            open_date TEXT NOT NULL,
            is_sent INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0,
            created_at TEXT,
            completed_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS surprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_opened INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            reminder_hour INTEGER,
            reminder_minute INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            is_done INTEGER DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            section TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS care_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

    _seed_default_data()


def _seed_default_data() -> None:
    conn = get_connection()
    c = conn.cursor()

    # Seed default compliments if empty
    c.execute("SELECT COUNT(*) FROM compliments")
    if c.fetchone()[0] == 0:
        compliments = [
            "Ты самая невероятная девушка на свете 💖",
            "Твоя улыбка освещает весь мир 🌟",
            "Ты сильнее, чем думаешь, и красивее, чем представляешь 🌸",
            "Каждый день с тобой — подарок ✨",
            "Ты заслуживаешь всего самого лучшего 💕",
            "Ты — настоящее чудо 🫶",
            "В тебе столько света и тепла 🌞",
            "Ты вдохновляешь просто тем, что ты есть 💫",
            "Мир стал лучше, потому что в нём есть ты 🌷",
            "Ты умная, красивая и невероятно добрая 💝",
        ]
        for text in compliments:
            c.execute(
                "INSERT INTO compliments (text, created_at) VALUES (?, ?)",
                (text, now_str()),
            )

    # Seed default support messages if empty
    c.execute("SELECT COUNT(*) FROM support_messages")
    if c.fetchone()[0] == 0:
        support = [
            ("грустно", "Эй, всё будет хорошо 💛 Я рядом, и ты не одна. Позволь себе погрустить, но помни — после дождя всегда выходит солнце 🌈"),
            ("грустно", "Обними себя покрепче 🤗 Ты справляешься лучше, чем думаешь. Я горжусь тобой 💖"),
            ("грустно", "Знаешь что? Ты невероятно сильная. Даже в трудные моменты ты остаёшься собой — и это прекрасно 🌸"),
            ("улыбнуться", "А ты знала, что выдры держатся за лапки, когда спят, чтобы не потеряться? 🦦💕"),
            ("улыбнуться", "Улыбнись! Ты прекрасна, когда улыбаешься 😊✨"),
            ("улыбнуться", "Представь, что тебя обнимает огромный пушистый кот 🐱💖 Стало теплее?"),
        ]
        for cat, text in support:
            c.execute(
                "INSERT INTO support_messages (category, text, created_at) VALUES (?, ?, ?)",
                (cat, text, now_str()),
            )

    # Seed default care messages if empty
    c.execute("SELECT COUNT(*) FROM care_messages")
    if c.fetchone()[0] == 0:
        care = [
            "Попей водички, солнышко 💧",
            "Сделай глубокий вдох и выдох 🌬️ Ты молодец!",
            "Потянись и расправь плечи 🧘‍♀️ Твоё тело тебе спасибо скажет!",
            "Закрой глаза на минутку и подумай о чём-то хорошем 🌸",
            "Ты давно ела? Позаботься о себе, покушай что-нибудь вкусное 🍰",
            "Обними себя покрепче — ты заслуживаешь тепла 🤗💖",
            "Может, пора отдохнуть? Ты и так делаешь много 🌙",
        ]
        for text in care:
            c.execute(
                "INSERT INTO care_messages (text, created_at) VALUES (?, ?)",
                (text, now_str()),
            )

    # Seed default schedule messages if empty
    c.execute("SELECT COUNT(*) FROM schedule_messages")
    if c.fetchone()[0] == 0:
        schedules = [
            ("morning", "Доброе утро, солнышко! ☀️ Пусть этот день будет наполнен радостью и теплом 🌸💖", 8, 0),
            ("night", "Спокойной ночи, моя звёздочка 🌙✨ Пусть тебе приснятся самые красивые сны 💤💕", 23, 0),
        ]
        for msg_type, text, hour, minute in schedules:
            c.execute(
                "INSERT INTO schedule_messages (type, text, hour, minute, created_at) VALUES (?, ?, ?, ?, ?)",
                (msg_type, text, hour, minute, now_str()),
            )

    # Seed default passwords if empty
    c.execute("SELECT COUNT(*) FROM passwords")
    if c.fetchone()[0] == 0:
        from bot.utils.security import hash_password

        sections = ["diary", "letters", "time_capsule", "memories", "surprises", "secrets"]
        default_pw = "1234"
        pw_hash = hash_password(default_pw)
        for section in sections:
            c.execute(
                "INSERT INTO passwords (section, password_hash) VALUES (?, ?)",
                (section, pw_hash),
            )

    conn.commit()
    conn.close()


# --- Query helpers ---

def add_user(user_id: int, username: str | None, first_name: str | None, role: str = "user") -> None:
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name, role, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, first_name, role, now_str()),
    )
    conn.commit()
    conn.close()


def get_user(user_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def get_random_compliment() -> str | None:
    conn = get_connection()
    row = conn.execute("SELECT text FROM compliments ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    return row["text"] if row else None


def add_compliment(text: str) -> None:
    conn = get_connection()
    conn.execute("INSERT INTO compliments (text, created_at) VALUES (?, ?)", (text, now_str()))
    conn.commit()
    conn.close()


def get_all_compliments() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM compliments ORDER BY id").fetchall()
    conn.close()
    return rows


def delete_compliment(comp_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM compliments WHERE id = ?", (comp_id,))
    conn.commit()
    conn.close()


def get_random_support(category: str) -> str | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT text FROM support_messages WHERE category = ? ORDER BY RANDOM() LIMIT 1",
        (category,),
    ).fetchone()
    conn.close()
    return row["text"] if row else None


def add_support_message(category: str, text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO support_messages (category, text, created_at) VALUES (?, ?, ?)",
        (category, text, now_str()),
    )
    conn.commit()
    conn.close()


def add_note(user_id: int, text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO notes (user_id, text, created_at) VALUES (?, ?, ?)",
        (user_id, text, now_str()),
    )
    conn.commit()
    conn.close()


def get_notes(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def delete_note(note_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


def add_diary_entry(user_id: int, text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO diary_entries (user_id, text, created_at) VALUES (?, ?, ?)",
        (user_id, text, now_str()),
    )
    conn.commit()
    conn.close()


def get_diary_entries(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM diary_entries WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def add_mood(user_id: int, mood: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO mood_logs (user_id, mood, created_at) VALUES (?, ?, ?)",
        (user_id, mood, now_str()),
    )
    conn.commit()
    conn.close()


def get_mood_history(user_id: int, limit: int = 30) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM mood_logs WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return rows


def add_letter(from_user_id: int, text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO letters (from_user_id, text, created_at) VALUES (?, ?, ?)",
        (from_user_id, text, now_str()),
    )
    conn.commit()
    conn.close()


def get_letters() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM letters ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def mark_letter_read(letter_id: int) -> None:
    conn = get_connection()
    conn.execute("UPDATE letters SET is_read = 1 WHERE id = ?", (letter_id,))
    conn.commit()
    conn.close()


def add_time_capsule(user_id: int, text: str, open_date: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO time_capsules (user_id, text, open_date, created_at) VALUES (?, ?, ?, ?)",
        (user_id, text, open_date, now_str()),
    )
    conn.commit()
    conn.close()


def get_pending_capsules() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM time_capsules WHERE is_sent = 0 AND open_date <= ?",
        (today_str(),),
    ).fetchall()
    conn.close()
    return rows


def get_user_capsules(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM time_capsules WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def mark_capsule_sent(capsule_id: int) -> None:
    conn = get_connection()
    conn.execute("UPDATE time_capsules SET is_sent = 1 WHERE id = ?", (capsule_id,))
    conn.commit()
    conn.close()


def add_memory(text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO memories (text, created_at) VALUES (?, ?)",
        (text, now_str()),
    )
    conn.commit()
    conn.close()


def get_memories() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM memories ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def add_achievement(user_id: int, text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO achievements (user_id, text, created_at) VALUES (?, ?, ?)",
        (user_id, text, now_str()),
    )
    conn.commit()
    conn.close()


def get_achievements(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM achievements WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def add_goal(title: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO goals (title, created_at) VALUES (?, ?)",
        (title, now_str()),
    )
    conn.commit()
    conn.close()


def get_goals() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM goals ORDER BY is_completed, id DESC").fetchall()
    conn.close()
    return rows


def complete_goal(goal_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE goals SET is_completed = 1, completed_at = ? WHERE id = ?",
        (now_str(), goal_id),
    )
    conn.commit()
    conn.close()


def add_surprise(text: str, password_hash: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO surprises (text, password_hash, created_at) VALUES (?, ?, ?)",
        (text, password_hash, now_str()),
    )
    conn.commit()
    conn.close()


def get_surprises() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM surprises ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def get_surprise(surprise_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM surprises WHERE id = ?", (surprise_id,)).fetchone()
    conn.close()
    return row


def mark_surprise_opened(surprise_id: int) -> None:
    conn = get_connection()
    conn.execute("UPDATE surprises SET is_opened = 1 WHERE id = ?", (surprise_id,))
    conn.commit()
    conn.close()


def add_secret(user_id: int, text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO secrets (user_id, text, created_at) VALUES (?, ?, ?)",
        (user_id, text, now_str()),
    )
    conn.commit()
    conn.close()


def get_secrets(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM secrets WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def add_habit(user_id: int, name: str, reminder_hour: int | None = None, reminder_minute: int | None = None) -> int:
    conn = get_connection()
    c = conn.execute(
        "INSERT INTO habits (user_id, name, reminder_hour, reminder_minute, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, name, reminder_hour, reminder_minute, now_str()),
    )
    habit_id = c.lastrowid
    conn.commit()
    conn.close()
    return habit_id


def get_habits(user_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM habits WHERE user_id = ? AND is_active = 1 ORDER BY id",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_all_active_habits() -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM habits WHERE is_active = 1 AND reminder_hour IS NOT NULL"
    ).fetchall()
    conn.close()
    return rows


def delete_habit(habit_id: int) -> None:
    conn = get_connection()
    conn.execute("UPDATE habits SET is_active = 0 WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()


def log_habit(habit_id: int, date: str | None = None) -> None:
    if date is None:
        date = today_str()
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM habit_logs WHERE habit_id = ? AND date = ?",
        (habit_id, date),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE habit_logs SET is_done = 1 WHERE id = ?", (existing["id"],)
        )
    else:
        conn.execute(
            "INSERT INTO habit_logs (habit_id, date, is_done) VALUES (?, ?, 1)",
            (habit_id, date),
        )
    conn.commit()
    conn.close()


def get_habit_logs(habit_id: int, limit: int = 30) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM habit_logs WHERE habit_id = ? ORDER BY date DESC LIMIT ?",
        (habit_id, limit),
    ).fetchall()
    conn.close()
    return rows


def get_habit_streak(habit_id: int) -> int:
    conn = get_connection()
    rows = conn.execute(
        "SELECT date FROM habit_logs WHERE habit_id = ? AND is_done = 1 ORDER BY date DESC",
        (habit_id,),
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    streak = 0
    current = now_local().date()
    for row in rows:
        log_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        diff = (current - log_date).days
        if diff == streak:
            streak += 1
        elif diff > streak:
            break
    return streak


def get_password_hash(section: str) -> str | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT password_hash FROM passwords WHERE section = ?", (section,)
    ).fetchone()
    conn.close()
    return row["password_hash"] if row else None


def set_password(section: str, password_hash: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO passwords (section, password_hash) VALUES (?, ?)",
        (section, password_hash),
    )
    conn.commit()
    conn.close()


def get_random_care_message() -> str | None:
    conn = get_connection()
    row = conn.execute("SELECT text FROM care_messages ORDER BY RANDOM() LIMIT 1").fetchone()
    conn.close()
    return row["text"] if row else None


def add_care_message(text: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO care_messages (text, created_at) VALUES (?, ?)",
        (text, now_str()),
    )
    conn.commit()
    conn.close()


def get_schedule_messages(msg_type: str) -> list[sqlite3.Row]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM schedule_messages WHERE type = ? AND is_active = 1",
        (msg_type,),
    ).fetchall()
    conn.close()
    return rows


def update_schedule_message(msg_id: int, text: str) -> None:
    conn = get_connection()
    conn.execute("UPDATE schedule_messages SET text = ? WHERE id = ?", (text, msg_id))
    conn.commit()
    conn.close()


def get_mood_stats(user_id: int, days: int = 30) -> dict[str, int]:
    from datetime import timedelta

    cutoff = (now_local() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    rows = conn.execute(
        """SELECT mood, COUNT(*) as cnt FROM mood_logs
        WHERE user_id = ? AND created_at >= ?
        GROUP BY mood""",
        (user_id, cutoff),
    ).fetchall()
    conn.close()
    return {row["mood"]: row["cnt"] for row in rows}


def get_habit_completion_rate(habit_id: int, days: int = 30) -> float:
    from datetime import timedelta

    cutoff = (now_local() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = get_connection()
    row = conn.execute(
        """SELECT COUNT(*) as done FROM habit_logs
        WHERE habit_id = ? AND is_done = 1 AND date >= ?""",
        (habit_id, cutoff),
    ).fetchone()
    conn.close()
    done = row["done"] if row else 0
    return (done / days) * 100 if days > 0 else 0.0


def get_goals_stats() -> dict[str, int]:
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) as cnt FROM goals").fetchone()["cnt"]
    completed = conn.execute(
        "SELECT COUNT(*) as cnt FROM goals WHERE is_completed = 1"
    ).fetchone()["cnt"]
    conn.close()
    return {"total": total, "completed": completed, "remaining": total - completed}
