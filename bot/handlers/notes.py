from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import notes_menu_kb, notes_delete_kb, cancel_kb
from bot.states.states import NotesStates

router = Router()


@router.message(F.text == "📝 Заметки")
async def notes_menu(message: Message) -> None:
    await message.answer("📝 Заметки\n\nВыбери действие:", reply_markup=notes_menu_kb())


@router.callback_query(F.data == "notes:add")
async def notes_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(NotesStates.waiting_text)
    await callback.message.answer("✏️ Напиши свою заметку:", reply_markup=cancel_kb())  # type: ignore[union-attr]
    await callback.answer()


@router.message(NotesStates.waiting_text)
async def notes_add_save(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, напиши текст заметки 📝")
        return
    db.add_note(message.from_user.id, message.text)  # type: ignore[union-attr]
    await state.clear()
    await message.answer("✅ Заметка сохранена! 📝", reply_markup=notes_menu_kb())


@router.callback_query(F.data == "notes:list")
async def notes_list(callback: CallbackQuery) -> None:
    notes = db.get_notes(callback.from_user.id)
    if not notes:
        await callback.message.answer("У тебя пока нет заметок 📝")  # type: ignore[union-attr]
        await callback.answer()
        return

    text = "📋 Твои заметки:\n\n"
    for i, note in enumerate(notes[:10], 1):
        text += f"{i}. {note['text']}\n   📅 {note['created_at']}\n\n"

    await callback.message.answer(text, reply_markup=notes_delete_kb(notes))  # type: ignore[union-attr]
    await callback.answer()


@router.callback_query(F.data.startswith("note:del:"))
async def notes_delete(callback: CallbackQuery) -> None:
    note_id = int(callback.data.split(":")[2])  # type: ignore[union-attr]
    db.delete_note(note_id)
    await callback.message.answer("🗑 Заметка удалена!")  # type: ignore[union-attr]
    await callback.answer()
