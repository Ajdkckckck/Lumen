from aiogram import Router, F
from aiogram.types import Message

from bot.database import db

router = Router()


@router.message(F.text == "💌 Комплимент")
async def send_compliment(message: Message) -> None:
    compliment = db.get_random_compliment()
    if compliment:
        await message.answer(f"💌 {compliment}")
    else:
        await message.answer("Пока нет комплиментов 😔 Но ты всё равно прекрасна! 💖")
