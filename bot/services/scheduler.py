import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

from bot.config import ADMIN_ID, TIMEZONE
from bot.database import db

logger = logging.getLogger(__name__)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    # Morning message
    morning_msgs = db.get_schedule_messages("morning")
    for msg in morning_msgs:
        scheduler.add_job(
            send_scheduled_message,
            CronTrigger(hour=msg["hour"], minute=msg["minute"], timezone=TIMEZONE),
            args=[bot, msg["text"]],
            id=f"morning_{msg['id']}",
            replace_existing=True,
        )

    # Night message
    night_msgs = db.get_schedule_messages("night")
    for msg in night_msgs:
        scheduler.add_job(
            send_scheduled_message,
            CronTrigger(hour=msg["hour"], minute=msg["minute"], timezone=TIMEZONE),
            args=[bot, msg["text"]],
            id=f"night_{msg['id']}",
            replace_existing=True,
        )

    # Check time capsules every hour
    scheduler.add_job(
        check_time_capsules,
        CronTrigger(minute=0, timezone=TIMEZONE),
        args=[bot],
        id="check_capsules",
        replace_existing=True,
    )

    # Habit reminders - check every minute
    scheduler.add_job(
        check_habit_reminders,
        CronTrigger(minute="*", timezone=TIMEZONE),
        args=[bot],
        id="habit_reminders",
        replace_existing=True,
    )

    return scheduler


async def send_scheduled_message(bot: Bot, text: str) -> None:
    """Send a scheduled message to all non-admin users."""
    try:
        conn = db.get_connection()
        users = conn.execute(
            "SELECT user_id FROM users WHERE user_id != ?", (ADMIN_ID,)
        ).fetchall()
        conn.close()

        for user in users:
            try:
                await bot.send_message(user["user_id"], text)
            except Exception as e:
                logger.error("Failed to send scheduled message to %s: %s", user["user_id"], e)
    except Exception as e:
        logger.error("Error in send_scheduled_message: %s", e)


async def check_time_capsules(bot: Bot) -> None:
    """Check and send due time capsules."""
    try:
        capsules = db.get_pending_capsules()
        for capsule in capsules:
            try:
                text = (
                    "📦 Капсула времени открыта! ✨\n\n"
                    f"💌 Сообщение из прошлого:\n{capsule['text']}\n\n"
                    f"📅 Создано: {capsule['created_at']}"
                )
                await bot.send_message(capsule["user_id"], text)
                db.mark_capsule_sent(capsule["id"])
            except Exception as e:
                logger.error("Failed to send capsule %s: %s", capsule["id"], e)
    except Exception as e:
        logger.error("Error in check_time_capsules: %s", e)


async def check_habit_reminders(bot: Bot) -> None:
    """Check and send habit reminders."""
    try:
        now = db.now_local()
        current_hour = now.hour
        current_minute = now.minute

        habits = db.get_all_active_habits()
        for habit in habits:
            if habit["reminder_hour"] == current_hour and habit["reminder_minute"] == current_minute:
                try:
                    text = (
                        f"⏰ Напоминание о привычке!\n\n"
                        f"💪 «{habit['name']}»\n\n"
                        f"Не забудь выполнить! Ты справишься! 💖"
                    )
                    await bot.send_message(habit["user_id"], text)
                except Exception as e:
                    logger.error("Failed to send habit reminder %s: %s", habit["id"], e)
    except Exception as e:
        logger.error("Error in check_habit_reminders: %s", e)
