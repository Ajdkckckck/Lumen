from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def main_menu_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="💌 Комплимент"), KeyboardButton(text="🫶 Поддержка")],
        [KeyboardButton(text="📓 Дневник"), KeyboardButton(text="📬 Письма")],
        [KeyboardButton(text="📖 Воспоминания"), KeyboardButton(text="😊 Настроение")],
        [KeyboardButton(text="🎯 Цели"), KeyboardButton(text="🏆 Достижения")],
        [KeyboardButton(text="💪 Привычки"), KeyboardButton(text="📦 Капсула времени")],
        [KeyboardButton(text="🎁 Сюрпризы"), KeyboardButton(text="🔐 Личные секреты")],
        [KeyboardButton(text="🧠 Режим заботы"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="📝 Заметки")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def admin_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Комплимент", callback_data="admin:add_compliment")],
        [InlineKeyboardButton(text="➕ Поддержка", callback_data="admin:add_support")],
        [InlineKeyboardButton(text="➕ Забота", callback_data="admin:add_care")],
        [InlineKeyboardButton(text="✉️ Письмо", callback_data="admin:send_letter")],
        [InlineKeyboardButton(text="🎁 Сюрприз", callback_data="admin:add_surprise")],
        [InlineKeyboardButton(text="📖 Воспоминание", callback_data="admin:add_memory")],
        [InlineKeyboardButton(text="🎯 Цель", callback_data="admin:add_goal")],
        [InlineKeyboardButton(text="🔑 Сменить пароль", callback_data="admin:change_password")],
        [InlineKeyboardButton(text="⏰ Расписание", callback_data="admin:schedule")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def support_categories_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="😢 Мне грустно", callback_data="support:грустно")],
        [InlineKeyboardButton(text="😊 Хочу улыбнуться", callback_data="support:улыбнуться")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def mood_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="😊", callback_data="mood:😊"),
            InlineKeyboardButton(text="😐", callback_data="mood:😐"),
            InlineKeyboardButton(text="😢", callback_data="mood:😢"),
            InlineKeyboardButton(text="😡", callback_data="mood:😡"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]]
    )


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад", callback_data="back")]]
    )


def notes_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📝 Добавить заметку", callback_data="notes:add")],
        [InlineKeyboardButton(text="📋 Мои заметки", callback_data="notes:list")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def diary_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="✏️ Новая запись", callback_data="diary:add")],
        [InlineKeyboardButton(text="📖 Читать дневник", callback_data="diary:list")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def goals_kb(goals: list) -> InlineKeyboardMarkup:
    buttons = []
    for goal in goals:
        status = "✅" if goal["is_completed"] else "⬜"
        buttons.append(
            [InlineKeyboardButton(
                text=f"{status} {goal['title']}",
                callback_data=f"goal:toggle:{goal['id']}",
            )]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def habits_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Новая привычка", callback_data="habits:add")],
        [InlineKeyboardButton(text="📋 Мои привычки", callback_data="habits:list")],
        [InlineKeyboardButton(text="✅ Отметить", callback_data="habits:check")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def habits_list_kb(habits: list) -> InlineKeyboardMarkup:
    buttons = []
    for habit in habits:
        buttons.append(
            [InlineKeyboardButton(
                text=f"✅ {habit['name']}",
                callback_data=f"habit:done:{habit['id']}",
            )]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def secrets_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="✏️ Записать секрет", callback_data="secrets:add")],
        [InlineKeyboardButton(text="📖 Мои секреты", callback_data="secrets:list")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def capsule_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="💌 Создать капсулу", callback_data="capsule:add")],
        [InlineKeyboardButton(text="📋 Мои капсулы", callback_data="capsule:list")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def surprises_list_kb(surprises: list) -> InlineKeyboardMarkup:
    buttons = []
    for s in surprises:
        status = "🎁" if not s["is_opened"] else "📭"
        buttons.append(
            [InlineKeyboardButton(
                text=f"{status} Сюрприз #{s['id']}",
                callback_data=f"surprise:open:{s['id']}",
            )]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def password_sections_kb() -> InlineKeyboardMarkup:
    sections = [
        ("📓 Дневник", "diary"),
        ("📬 Письма", "letters"),
        ("📦 Капсула времени", "time_capsule"),
        ("📖 Воспоминания", "memories"),
        ("🎁 Сюрпризы", "surprises"),
        ("🔐 Секреты", "secrets"),
    ]
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"pwd_section:{key}")]
        for name, key in sections
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def achievements_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Добавить достижение", callback_data="achieve:add")],
        [InlineKeyboardButton(text="📋 Мои достижения", callback_data="achieve:list")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def notes_delete_kb(notes: list) -> InlineKeyboardMarkup:
    buttons = []
    for note in notes[:10]:
        short = note["text"][:30] + ("..." if len(note["text"]) > 30 else "")
        buttons.append(
            [InlineKeyboardButton(
                text=f"🗑 {short}",
                callback_data=f"note:del:{note['id']}",
            )]
        )
    buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_support_category_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="😢 Грустно", callback_data="admin_sup_cat:грустно")],
        [InlineKeyboardButton(text="😊 Улыбнуться", callback_data="admin_sup_cat:улыбнуться")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
