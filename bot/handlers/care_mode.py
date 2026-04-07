from aiogram import Router, F
from aiogram.types import Message

from bot.database import db

router = Router()


@router.message(F.text == "🧠 Режим заботы")
async def care_mode(message: Message) -> None:
    care_text = db.get_random_care_message()
    if care_text:
        await message.answer(f"🫶 {care_text}")
    else:
        await message.answer(
            "Солнышко, помни — ты важна и любима 💖\n"
            "Попей водички, потянись и улыбнись 🌸"
        )
