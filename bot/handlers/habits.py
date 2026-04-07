from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.database import db
from bot.keyboards.menus import habits_menu_kb, habits_list_kb, cancel_kb
from bot.states.states import HabitsStates

router = Router()


@router.message(F.text == "💪 Привычки")
async def habits_menu(message: Message) -> None:
    await message.answer(
        "💪 Привычки и дисциплина\n\nВыбери действие:",
        reply_markup=habits_menu_kb(),
    )


@router.callback_query(F.data == "habits:add")
async def habits_add_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(HabitsStates.waiting_name)
    await callback.message.answer(  # type: ignore[union-attr]
        "💪 Напиши название привычки:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(HabitsStates.waiting_name)
async def habits_add_name(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Пожалуйста, напиши название привычки 💪")
        return
    await state.update_data(habit_name=message.text)
    await state.set_state(HabitsStates.waiting_reminder_time)
    await message.answer(
        "⏰ Установить напоминание?\n\n"
        "Напиши время в формате ЧЧ:ММ (по Уфе)\n"
        "Или отправь «нет» без напоминания:",
        reply_markup=cancel_kb(),
    )


@router.message(HabitsStates.waiting_reminder_time)
async def habits_add_time(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer("Напиши время или «нет»:")
        return

    data = await state.get_data()
    habit_name = data["habit_name"]
    reminder_hour = None
    reminder_minute = None

    if message.text.lower().strip() != "нет":
        try:
            parts = message.text.strip().split(":")
            reminder_hour = int(parts[0])
            reminder_minute = int(parts[1])
            if not (0 <= reminder_hour <= 23 and 0 <= reminder_minute <= 59):
                raise ValueError
        except (ValueError, IndexError):
            await message.answer("❌ Неверный формат! Используй ЧЧ:ММ или «нет»")
            return

    db.add_habit(
        message.from_user.id,  # type: ignore[union-attr]
        habit_name,
        reminder_hour,
        reminder_minute,
    )
    await state.clear()

    time_text = ""
    if reminder_hour is not None:
        time_text = f"\n⏰ Напоминание: {reminder_hour:02d}:{reminder_minute:02d}"

    await message.answer(
        f"✅ Привычка «{habit_name}» добавлена! 💪{time_text}",
        reply_markup=habits_menu_kb(),
    )


@router.callback_query(F.data == "habits:list")
async def habits_list(callback: CallbackQuery) -> None:
    habits = db.get_habits(callback.from_user.id)
    if not habits:
        await callback.message.answer(  # type: ignore[union-attr]
            "У тебя пока нет привычек 💪\nДобавь первую!"
        )
        await callback.answer()
        return

    text = "📋 Твои привычки:\n\n"
    for habit in habits:
        streak = db.get_habit_streak(habit["id"])
        rate = db.get_habit_completion_rate(habit["id"])
        time_str = ""
        if habit["reminder_hour"] is not None:
            time_str = f" ⏰ {habit['reminder_hour']:02d}:{habit['reminder_minute']:02d}"
        text += (
            f"💪 {habit['name']}{time_str}\n"
            f"   🔥 Серия: {streak} дн. | 📊 {rate:.0f}%\n\n"
        )

    await callback.message.answer(text)  # type: ignore[union-attr]
    await callback.answer()


@router.callback_query(F.data == "habits:check")
async def habits_check(callback: CallbackQuery) -> None:
    habits = db.get_habits(callback.from_user.id)
    if not habits:
        await callback.message.answer("У тебя пока нет привычек 💪")  # type: ignore[union-attr]
        await callback.answer()
        return

    await callback.message.answer(  # type: ignore[union-attr]
        "✅ Отметь выполненные привычки:",
        reply_markup=habits_list_kb(habits),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("habit:done:"))
async def habit_done(callback: CallbackQuery) -> None:
    habit_id = int(callback.data.split(":")[2])  # type: ignore[union-attr]
    db.log_habit(habit_id)
    streak = db.get_habit_streak(habit_id)
    await callback.message.answer(  # type: ignore[union-attr]
        f"✅ Отлично! Привычка отмечена! 💪\n🔥 Текущая серия: {streak} дн."
    )
    await callback.answer()
