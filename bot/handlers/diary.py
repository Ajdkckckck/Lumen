from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import diary_menu_kb, cancel_kb
from bot.states.states import DiaryStates
from bot.utils.security import verify_password

router = Router()


@router.message(F.text == "📓 Дневник")
async def diary_start(message: Message, state: FSMContext) -> None:
    await state.set_state(DiaryStates.waiting_password)
    await state.update_data(section="diary")
    await message.answer("🔐 Введи пароль для доступа к дневнику:", reply_markup=cancel_kb())


@router.message(DiaryStates.waiting_password)
async def diary_check_password(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    pw_hash = db.get_password_hash("diary")
    if not pw_hash or not verify_password(message.text, pw_hash):
        await state.clear()
        await message.answer("❌ Неверный пароль!")
        return

    await state.set_state(None)
    await message.answer(
        "📓 Дневник открыт! 💖\n\nВыбери действие:",
        reply_markup=diary_menu_kb(),
    )


@router.callback_query(F.data == "diary:add")
async def diary_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DiaryStates.waiting_entry)
    await callback.message.answer(  # type: ignore[union-attr]
        "✏️ Напиши свою запись в дневник:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(DiaryStates.waiting_entry)
async def diary_add_save(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, напиши текст записи 📝")
        return
    db.add_diary_entry(message.from_user.id, message.text)  # type: ignore[union-attr]
    await state.clear()
    await message.answer("✅ Запись добавлена в дневник! 📓💖", reply_markup=diary_menu_kb())


@router.callback_query(F.data == "diary:list")
async def diary_list(callback: CallbackQuery) -> None:
    entries = db.get_diary_entries(callback.from_user.id)
    if not entries:
        await callback.message.answer("Дневник пока пуст 📓 Начни писать!")  # type: ignore[union-attr]
        await callback.answer()
        return

    text = "📓 Твой дневник:\n\n"
    for i, entry in enumerate(entries[:10], 1):
        text += f"📅 {entry['created_at']}\n{entry['text']}\n\n{'—' * 20}\n\n"

    await callback.message.answer(text)  # type: ignore[union-attr]
    await callback.answer()
