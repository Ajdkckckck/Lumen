from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import capsule_menu_kb, cancel_kb
from bot.states.states import TimeCapsuleStates
from bot.utils.security import verify_password

router = Router()


@router.message(F.text == "📦 Капсула времени")
async def capsule_start(message: Message, state: FSMContext) -> None:
    await state.set_state(TimeCapsuleStates.waiting_password)
    await message.answer(
        "🔐 Введи пароль для доступа к капсуле времени:",
        reply_markup=cancel_kb(),
    )


@router.message(TimeCapsuleStates.waiting_password)
async def capsule_check_password(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    pw_hash = db.get_password_hash("time_capsule")
    if not pw_hash or not verify_password(message.text, pw_hash):
        await state.clear()
        await message.answer("❌ Неверный пароль!")
        return

    await state.set_state(None)
    await message.answer(
        "📦 Капсула времени открыта! ✨\n\nВыбери действие:",
        reply_markup=capsule_menu_kb(),
    )


@router.callback_query(F.data == "capsule:add")
async def capsule_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(TimeCapsuleStates.waiting_message)
    await callback.message.answer(  # type: ignore[union-attr]
        "💌 Напиши сообщение для будущей себя:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(TimeCapsuleStates.waiting_message)
async def capsule_add_message(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, напиши сообщение 💌")
        return
    await state.update_data(capsule_text=message.text)
    await state.set_state(TimeCapsuleStates.waiting_date)
    await message.answer(
        "📅 Когда открыть капсулу?\n"
        "Напиши дату в формате: ДД.ММ.ГГГГ\n"
        "Например: 31.12.2025",
        reply_markup=cancel_kb(),
    )


@router.message(TimeCapsuleStates.waiting_date)
async def capsule_add_date(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи дату:")
        return

    try:
        from datetime import datetime

        date_obj = datetime.strptime(message.text.strip(), "%d.%m.%Y")
        open_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        await message.answer("❌ Неверный формат даты! Используй: ДД.ММ.ГГГГ")
        return

    data = await state.get_data()
    capsule_text = data.get("capsule_text", "")
    db.add_time_capsule(message.from_user.id, capsule_text, open_date)  # type: ignore[union-attr]
    await state.clear()
    await message.answer(
        f"✅ Капсула времени создана! 📦\n"
        f"Она откроется {message.text.strip()} ✨",
        reply_markup=capsule_menu_kb(),
    )


@router.callback_query(F.data == "capsule:list")
async def capsule_list(callback: CallbackQuery) -> None:
    capsules = db.get_user_capsules(callback.from_user.id)
    if not capsules:
        await callback.message.answer("У тебя пока нет капсул времени 📦")  # type: ignore[union-attr]
        await callback.answer()
        return

    text = "📦 Твои капсулы времени:\n\n"
    for cap in capsules[:10]:
        status = "📬 Отправлена" if cap["is_sent"] else f"⏳ Откроется {cap['open_date']}"
        text += f"💌 {cap['text'][:50]}...\n{status}\n📅 Создана: {cap['created_at']}\n\n"

    await callback.message.answer(text)  # type: ignore[union-attr]
    await callback.answer()
