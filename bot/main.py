import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.database.db import init_db
from bot.handlers import (
    start,
    compliments,
    support,
    notes,
    diary,
    mood,
    letters,
    time_capsule,
    memories,
    achievements,
    goals,
    surprises,
    secrets,
    care_mode,
    habits,
    statistics,
    admin,
    cancel,
)
from bot.services.scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set! Please set it in .env file.")
        sys.exit(1)

    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Create bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers (order matters for FSM)
    dp.include_router(cancel.router)
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(compliments.router)
    dp.include_router(support.router)
    dp.include_router(notes.router)
    dp.include_router(diary.router)
    dp.include_router(mood.router)
    dp.include_router(letters.router)
    dp.include_router(time_capsule.router)
    dp.include_router(memories.router)
    dp.include_router(achievements.router)
    dp.include_router(goals.router)
    dp.include_router(surprises.router)
    dp.include_router(secrets.router)
    dp.include_router(care_mode.router)
    dp.include_router(habits.router)
    dp.include_router(statistics.router)

    # Setup scheduler
    scheduler = setup_scheduler(bot)
    scheduler.start()
    logger.info("Scheduler started")

    # Start polling
    logger.info("Bot is starting...")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
