from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import support_categories_kb

router = Router()


@router.message(F.text == "🫶 Поддержка")
async def support_menu(message: Message) -> None:
    await message.answer(
        "Как ты себя чувствуешь? 💛\nВыбери категорию:",
        reply_markup=support_categories_kb(),
    )


@router.callback_query(F.data.startswith("support:"))
async def support_response(callback: CallbackQuery) -> None:
    category = callback.data.split(":")[1]  # type: ignore[union-attr]
    text = db.get_random_support(category)
    if text:
        await callback.message.answer(text)  # type: ignore[union-attr]
    else:
        await callback.message.answer("Я рядом, солнышко 💖 Всё будет хорошо!")  # type: ignore[union-attr]
    await callback.answer()
