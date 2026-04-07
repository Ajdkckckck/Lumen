from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import db
from bot.keyboards.menus import cancel_kb
from bot.states.states import MemoriesStates
from bot.utils.security import verify_password

router = Router()


@router.message(F.text == "📖 Воспоминания")
async def memories_start(message: Message, state: FSMContext) -> None:
    await state.set_state(MemoriesStates.waiting_password)
    await message.answer(
        "🔐 Введи пароль для доступа к воспоминаниям:",
        reply_markup=cancel_kb(),
    )


@router.message(MemoriesStates.waiting_password)
async def memories_check_password(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    pw_hash = db.get_password_hash("memories")
    if not pw_hash or not verify_password(message.text, pw_hash):
        await state.clear()
        await message.answer("❌ Неверный пароль!")
        return

    await state.clear()
    memories = db.get_memories()
    if not memories:
        await message.answer("📖 Пока нет воспоминаний. Но они обязательно появятся! 🌸")
        return

    text = "📖 Воспоминания:\n\n"
    for mem in memories[:10]:
        text += f"🌸 {mem['text']}\n📅 {mem['created_at']}\n\n{'—' * 20}\n\n"

    await message.answer(text)
