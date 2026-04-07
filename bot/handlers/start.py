from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.config import ADMIN_ID
from bot.database import db
from bot.keyboards.menus import main_menu_kb, admin_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    if not user:
        return

    role = "admin" if user.id == ADMIN_ID else "user"
    db.add_user(user.id, user.username, user.first_name, role)

    name = user.first_name or "солнышко"
    text = (
        f"Привет, {name}! 💖\n\n"
        "Я — ЛЮМИ, твой персональный бот заботы и поддержки 🌸\n\n"
        "Я буду рядом, чтобы поднять настроение, "
        "хранить твои мысли и помогать с целями ✨\n\n"
        "Выбери, что тебе нужно, из меню ниже 👇"
    )
    await message.answer(text, reply_markup=main_menu_kb(show_admin=(role == "admin")))


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    user = message.from_user
    if not user or user.id != ADMIN_ID:
        await message.answer("⛔ У тебя нет доступа к этой команде.")
        return

    await message.answer(
        "🛠 Панель администратора\n\nВыбери действие:",
        reply_markup=admin_menu_kb(),
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    user = message.from_user
    is_adm = user is not None and user.id == ADMIN_ID
    await message.answer("Главное меню 💖", reply_markup=main_menu_kb(show_admin=is_adm))


@router.message(F.text == "🛠 Админ-панель")
async def btn_admin(message: Message) -> None:
    user = message.from_user
    if not user or user.id != ADMIN_ID:
        await message.answer("⛔ У тебя нет доступа к этой команде.")
        return
    await message.answer(
        "🛠 Панель администратора\n\nВыбери действие:",
        reply_markup=admin_menu_kb(),
    )
