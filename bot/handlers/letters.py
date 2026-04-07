from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database import db
from bot.keyboards.menus import cancel_kb
from bot.states.states import LettersStates
from bot.utils.security import verify_password

router = Router()


@router.message(F.text == "📬 Письма")
async def letters_start(message: Message, state: FSMContext) -> None:
    await state.set_state(LettersStates.waiting_password)
    await message.answer("🔐 Введи пароль для доступа к письмам:", reply_markup=cancel_kb())


@router.message(LettersStates.waiting_password)
async def letters_check_password(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    pw_hash = db.get_password_hash("letters")
    if not pw_hash or not verify_password(message.text, pw_hash):
        await state.clear()
        await message.answer("❌ Неверный пароль!")
        return

    await state.clear()
    letters = db.get_letters()
    if not letters:
        await message.answer("📬 Пока нет писем. Но скоро будут! 💌")
        return

    text = "📬 Твои письма:\n\n"
    for letter in letters[:10]:
        status = "📖" if letter["is_read"] else "💌"
        text += f"{status} Письмо от {letter['created_at']}:\n{letter['text']}\n\n{'—' * 20}\n\n"
        if not letter["is_read"]:
            db.mark_letter_read(letter["id"])

    await message.answer(text)
