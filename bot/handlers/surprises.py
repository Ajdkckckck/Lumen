from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import surprises_list_kb, cancel_kb
from bot.states.states import SurprisesStates
from bot.utils.security import verify_password

router = Router()


@router.message(F.text == "🎁 Сюрпризы")
async def surprises_start(message: Message, state: FSMContext) -> None:
    await state.set_state(SurprisesStates.waiting_password)
    await message.answer(
        "🔐 Введи пароль для доступа к сюрпризам:",
        reply_markup=cancel_kb(),
    )


@router.message(SurprisesStates.waiting_password)
async def surprises_check_password(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    pw_hash = db.get_password_hash("surprises")
    if not pw_hash or not verify_password(message.text, pw_hash):
        await state.clear()
        await message.answer("❌ Неверный пароль!")
        return

    await state.clear()
    surprises = db.get_surprises()
    if not surprises:
        await message.answer("🎁 Пока нет сюрпризов. Но что-то готовится! ✨")
        return

    await message.answer(
        "🎁 Твои сюрпризы:\n\nВыбери, чтобы открыть:",
        reply_markup=surprises_list_kb(surprises),
    )


@router.callback_query(F.data.startswith("surprise:open:"))
async def surprise_open(callback: CallbackQuery, state: FSMContext) -> None:
    surprise_id = int(callback.data.split(":")[2])  # type: ignore[union-attr]
    surprise = db.get_surprise(surprise_id)
    if not surprise:
        await callback.message.answer("❌ Сюрприз не найден.")  # type: ignore[union-attr]
        await callback.answer()
        return

    if surprise["is_opened"]:
        await callback.message.answer(  # type: ignore[union-attr]
            f"📭 Этот сюрприз уже был открыт:\n\n{surprise['text']}"
        )
        await callback.answer()
        return

    await state.update_data(surprise_id=surprise_id)
    await state.set_state(SurprisesStates.waiting_surprise_password)
    await callback.message.answer(  # type: ignore[union-attr]
        "🔑 Введи пароль от этого сюрприза:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(SurprisesStates.waiting_surprise_password)
async def surprise_unlock(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, введи пароль:")
        return

    data = await state.get_data()
    surprise_id = data.get("surprise_id")
    if not surprise_id:
        await state.clear()
        await message.answer("❌ Ошибка: сюрприз не выбран.")
        return

    surprise = db.get_surprise(surprise_id)
    if not surprise:
        await state.clear()
        await message.answer("❌ Сюрприз не найден.")
        return

    if not verify_password(message.text, surprise["password_hash"]):
        await state.clear()
        await message.answer("❌ Неверный пароль от сюрприза!")
        return

    db.mark_surprise_opened(surprise_id)
    await state.clear()
    await message.answer(
        f"🎉 Сюрприз открыт! 🎁✨\n\n{surprise['text']}"
    )
