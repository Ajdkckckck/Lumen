from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import achievements_menu_kb, cancel_kb
from bot.states.states import AchievementsStates

router = Router()


@router.message(F.text == "🏆 Достижения")
async def achievements_menu(message: Message) -> None:
    await message.answer(
        "🏆 Достижения\n\nВыбери действие:",
        reply_markup=achievements_menu_kb(),
    )


@router.callback_query(F.data == "achieve:add")
async def achieve_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AchievementsStates.waiting_text)
    await callback.message.answer(  # type: ignore[union-attr]
        "🏆 Напиши своё достижение:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(AchievementsStates.waiting_text)
async def achieve_add_save(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, напиши своё достижение 🏆")
        return
    db.add_achievement(message.from_user.id, message.text)  # type: ignore[union-attr]
    await state.clear()
    await message.answer(
        "✅ Достижение записано! Ты молодец! 🏆💖",
        reply_markup=achievements_menu_kb(),
    )


@router.callback_query(F.data == "achieve:list")
async def achieve_list(callback: CallbackQuery) -> None:
    achievements = db.get_achievements(callback.from_user.id)
    if not achievements:
        await callback.message.answer(  # type: ignore[union-attr]
            "У тебя пока нет записанных достижений 🏆\nНо ты точно уже многого добилась! 💖"
        )
        await callback.answer()
        return

    text = "🏆 Твои достижения:\n\n"
    for i, ach in enumerate(achievements[:15], 1):
        text += f"{i}. {ach['text']}\n   📅 {ach['created_at']}\n\n"

    await callback.message.answer(text)  # type: ignore[union-attr]
    await callback.answer()
