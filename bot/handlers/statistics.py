from aiogram import Router, F
from aiogram.types import Message

from bot.database import db

router = Router()


@router.message(F.text == "📊 Статистика")
async def statistics(message: Message) -> None:
    user_id = message.from_user.id  # type: ignore[union-attr]
    text = "📊 Твоя статистика\n\n"

    # Mood stats
    mood_stats = db.get_mood_stats(user_id)
    if mood_stats:
        text += "😊 Настроение за 30 дней:\n"
        mood_names = {"😊": "Радость", "😐": "Нормально", "😢": "Грусть", "😡": "Злость"}
        for mood, count in mood_stats.items():
            name = mood_names.get(mood, mood)
            bar = "█" * min(count, 20)
            text += f"  {mood} {name}: {bar} ({count})\n"
        text += "\n"

    # Goals stats
    goals_stats = db.get_goals_stats()
    if goals_stats["total"] > 0:
        text += "🎯 Цели:\n"
        text += f"  Всего: {goals_stats['total']}\n"
        text += f"  ✅ Выполнено: {goals_stats['completed']}\n"
        text += f"  ⏳ Осталось: {goals_stats['remaining']}\n"
        if goals_stats["total"] > 0:
            pct = (goals_stats["completed"] / goals_stats["total"]) * 100
            text += f"  📈 Прогресс: {pct:.0f}%\n"
        text += "\n"

    # Habits stats
    habits = db.get_habits(user_id)
    if habits:
        text += "💪 Привычки:\n"
        for habit in habits:
            streak = db.get_habit_streak(habit["id"])
            rate = db.get_habit_completion_rate(habit["id"])
            text += f"  {habit['name']}: 🔥{streak} дн. | {rate:.0f}%\n"
        text += "\n"

    # Diary & achievements counts
    diary_entries = db.get_diary_entries(user_id)
    achievements = db.get_achievements(user_id)
    notes = db.get_notes(user_id)

    text += "📈 Общая активность:\n"
    text += f"  📓 Записей в дневнике: {len(diary_entries)}\n"
    text += f"  🏆 Достижений: {len(achievements)}\n"
    text += f"  📝 Заметок: {len(notes)}\n"

    if not mood_stats and goals_stats["total"] == 0 and not habits:
        text += "\n💛 Начни пользоваться ботом, чтобы видеть свою статистику!"

    await message.answer(text)
