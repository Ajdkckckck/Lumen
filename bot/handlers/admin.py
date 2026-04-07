from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import ADMIN_ID
from bot.database import db
from bot.keyboards.menus import (
    admin_menu_kb,
    admin_support_category_kb,
    cancel_kb,
    password_sections_kb,
)
from bot.states.states import AdminStates
from bot.utils.security import hash_password

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# --- Add compliment ---

@router.callback_query(F.data == "admin:add_compliment")
async def admin_add_compliment(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await state.set_state(AdminStates.waiting_compliment)
    await callback.message.answer("💌 Напиши новый комплимент:", reply_markup=cancel_kb())  # type: ignore[union-attr]
    await callback.answer()


@router.message(AdminStates.waiting_compliment)
async def admin_save_compliment(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    db.add_compliment(message.text)
    await state.clear()
    await message.answer("✅ Комплимент добавлен! 💌", reply_markup=admin_menu_kb())


# --- Add support message ---

@router.callback_query(F.data == "admin:add_support")
async def admin_add_support(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await callback.message.answer(  # type: ignore[union-attr]
        "Выбери категорию:", reply_markup=admin_support_category_kb()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_sup_cat:"))
async def admin_support_category(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    category = callback.data.split(":")[1]  # type: ignore[union-attr]
    await state.update_data(support_category=category)
    await state.set_state(AdminStates.waiting_support_text)
    await callback.message.answer(  # type: ignore[union-attr]
        f"Напиши текст поддержки для категории «{category}»:",
        reply_markup=cancel_kb(),
    )
    await callback.answer()


@router.message(AdminStates.waiting_support_text)
async def admin_save_support(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    data = await state.get_data()
    category = data.get("support_category", "грустно")
    db.add_support_message(category, message.text)
    await state.clear()
    await message.answer("✅ Текст поддержки добавлен! 🫶", reply_markup=admin_menu_kb())


# --- Add care message ---

@router.callback_query(F.data == "admin:add_care")
async def admin_add_care(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await state.set_state(AdminStates.waiting_care_text)
    await callback.message.answer(  # type: ignore[union-attr]
        "🧠 Напиши текст заботы:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(AdminStates.waiting_care_text)
async def admin_save_care(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    db.add_care_message(message.text)
    await state.clear()
    await message.answer("✅ Текст заботы добавлен! 🧠", reply_markup=admin_menu_kb())


# --- Send letter ---

@router.callback_query(F.data == "admin:send_letter")
async def admin_send_letter(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await state.set_state(AdminStates.waiting_letter_text)
    await callback.message.answer(  # type: ignore[union-attr]
        "✉️ Напиши письмо:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(AdminStates.waiting_letter_text)
async def admin_save_letter(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    db.add_letter(message.from_user.id, message.text)  # type: ignore[union-attr]
    await state.clear()
    await message.answer("✅ Письмо отправлено! 📬💌", reply_markup=admin_menu_kb())


# --- Add surprise ---

@router.callback_query(F.data == "admin:add_surprise")
async def admin_add_surprise(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await state.set_state(AdminStates.waiting_surprise_text)
    await callback.message.answer(  # type: ignore[union-attr]
        "🎁 Напиши текст сюрприза:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(AdminStates.waiting_surprise_text)
async def admin_surprise_text(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    await state.update_data(surprise_text=message.text)
    await state.set_state(AdminStates.waiting_surprise_password)
    await message.answer(
        "🔑 Теперь задай пароль для этого сюрприза:",
        reply_markup=cancel_kb(),
    )


@router.message(AdminStates.waiting_surprise_password)
async def admin_save_surprise(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    data = await state.get_data()
    surprise_text = data.get("surprise_text", "")
    pw_hash = hash_password(message.text)
    db.add_surprise(surprise_text, pw_hash)
    await state.clear()
    await message.answer("✅ Сюрприз создан! 🎁✨", reply_markup=admin_menu_kb())


# --- Add memory ---

@router.callback_query(F.data == "admin:add_memory")
async def admin_add_memory(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await state.set_state(AdminStates.waiting_memory_text)
    await callback.message.answer(  # type: ignore[union-attr]
        "📖 Напиши воспоминание:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(AdminStates.waiting_memory_text)
async def admin_save_memory(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    db.add_memory(message.text)
    await state.clear()
    await message.answer("✅ Воспоминание добавлено! 📖🌸", reply_markup=admin_menu_kb())


# --- Add goal ---

@router.callback_query(F.data == "admin:add_goal")
async def admin_add_goal(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await state.set_state(AdminStates.waiting_goal_title)
    await callback.message.answer(  # type: ignore[union-attr]
        "🎯 Напиши название цели:", reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(AdminStates.waiting_goal_title)
async def admin_save_goal(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    db.add_goal(message.text)
    await state.clear()
    await message.answer("✅ Цель добавлена! 🎯", reply_markup=admin_menu_kb())


# --- Change password ---

@router.callback_query(F.data == "admin:change_password")
async def admin_change_password(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    await callback.message.answer(  # type: ignore[union-attr]
        "🔑 Выбери раздел для смены пароля:",
        reply_markup=password_sections_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("pwd_section:"))
async def admin_select_section(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return
    section = callback.data.split(":")[1]  # type: ignore[union-attr]
    await state.update_data(password_section=section)
    await state.set_state(AdminStates.waiting_new_password)
    await callback.message.answer(  # type: ignore[union-attr]
        f"🔑 Введи новый пароль для раздела «{section}»:",
        reply_markup=cancel_kb(),
    )
    await callback.answer()


@router.message(AdminStates.waiting_new_password)
async def admin_save_password(message: Message, state: FSMContext) -> None:
    if not message.text or not is_admin(message.from_user.id):  # type: ignore[union-attr]
        return
    data = await state.get_data()
    section = data.get("password_section", "")
    pw_hash = hash_password(message.text)
    db.set_password(section, pw_hash)
    await state.clear()
    await message.answer(
        f"✅ Пароль для «{section}» изменён! 🔑",
        reply_markup=admin_menu_kb(),
    )


# --- Schedule management ---

@router.callback_query(F.data == "admin:schedule")
async def admin_schedule(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет доступа")
        return

    morning = db.get_schedule_messages("morning")
    night = db.get_schedule_messages("night")

    text = "⏰ Расписание авто-сообщений:\n\n"

    if morning:
        for m in morning:
            text += f"☀️ Доброе утро ({m['hour']:02d}:{m['minute']:02d}):\n{m['text']}\n\n"
    if night:
        for n in night:
            text += f"🌙 Спокойной ночи ({n['hour']:02d}:{n['minute']:02d}):\n{n['text']}\n\n"

    text += "Для изменения используйте команды:\n/set_morning <текст>\n/set_night <текст>"
    await callback.message.answer(text)  # type: ignore[union-attr]
    await callback.answer()
