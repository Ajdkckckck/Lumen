from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import goals_kb

router = Router()


@router.message(F.text == "🎯 Цели")
async def goals_menu(message: Message) -> None:
    goals = db.get_goals()
    if not goals:
        await message.answer(
            "🎯 Пока нет целей.\n"
            "Попроси админа добавить цели для тебя! 💖"
        )
        return

    text = "🎯 Твои цели:\n\nНажми на цель, чтобы отметить выполнение:"
    await message.answer(text, reply_markup=goals_kb(goals))


@router.callback_query(F.data.startswith("goal:toggle:"))
async def goal_toggle(callback: CallbackQuery) -> None:
    goal_id = int(callback.data.split(":")[2])  # type: ignore[union-attr]
    db.complete_goal(goal_id)
    await callback.message.answer("✅ Цель выполнена! Ты молодец! 🎯💖")  # type: ignore[union-attr]

    # Refresh goals list
    goals = db.get_goals()
    if goals:
        await callback.message.answer(  # type: ignore[union-attr]
            "🎯 Обновлённый список целей:",
            reply_markup=goals_kb(goals),
        )
    await callback.answer()
