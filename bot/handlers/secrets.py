from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import secrets_menu_kb, cancel_kb
from bot.states.states import SecretsStates
from bot.utils.security import verify_password

router = Router()


@router.message(F.text == "🔐 Личные секреты")
async def secrets_start(message: Message, state: FSMContext) -> None:
    await state.set_state(SecretsStates.waiting_password)
    await message.answer(
        "🔐 Введи пароль для доступа к личным секретам:",
        reply_markup=cancel_kb(),
    )


@router.message(SecretsStates.waiting_password)
async def secrets_check_password(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    pw_hash = db.get_password_hash("secrets")
    if not pw_hash or not verify_password(message.text, pw_hash):
        await state.clear()
        await message.answer("❌ Неверный пароль!")
        return

    await state.set_state(None)
    await message.answer(
        "🔐 Доступ к секретам открыт! 💖\n\nВыбери действие:",
        reply_markup=secrets_menu_kb(),
    )


@router.callback_query(F.data == "secrets:add")
async def secrets_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SecretsStates.waiting_entry)
    await callback.message.answer(  # type: ignore[union-attr]
        "🤫 Напиши свой секрет:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(SecretsStates.waiting_entry)
async def secrets_add_save(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, напиши свой секрет 🤫")
        return
    db.add_secret(message.from_user.id, message.text)  # type: ignore[union-attr]
    await state.clear()
    await message.answer("✅ Секрет надёжно сохранён! 🔐💖", reply_markup=secrets_menu_kb())


@router.callback_query(F.data == "secrets:list")
async def secrets_list(callback: CallbackQuery) -> None:
    secrets = db.get_secrets(callback.from_user.id)
    if not secrets:
        await callback.message.answer("У тебя пока нет секретов 🔐")  # type: ignore[union-attr]
        await callback.answer()
        return

    text = "🔐 Твои секреты:\n\n"
    for i, secret in enumerate(secrets[:10], 1):
        text += f"{i}. {secret['text']}\n   📅 {secret['created_at']}\n\n"

    await callback.message.answer(text)  # type: ignore[union-attr]
    await callback.answer()
