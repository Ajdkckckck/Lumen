from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import mood_kb

router = Router()

MOOD_LABELS = {
    "😊": "радость",
    "😐": "нормально",
    "😢": "грусть",
    "😡": "злость",
}


@router.message(F.text == "😊 Настроение")
async def mood_menu(message: Message) -> None:
    await message.answer(
        "Как ты себя сейчас чувствуешь? 💛\nВыбери своё настроение:",
        reply_markup=mood_kb(),
    )


@router.callback_query(F.data.startswith("mood:"))
async def mood_save(callback: CallbackQuery) -> None:
    mood = callback.data.split(":")[1]  # type: ignore[union-attr]
    db.add_mood(callback.from_user.id, mood)
    label = MOOD_LABELS.get(mood, mood)
    await callback.message.answer(  # type: ignore[union-attr]
        f"Записала твоё настроение: {mood} ({label}) 💖\n\n"
        "Спасибо, что делишься! Я всегда рядом 🫶"
    )
    await callback.answer()
