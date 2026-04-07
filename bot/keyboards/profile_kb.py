from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Profile keyboard
profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👤 Мой профиль", callback_data="view_profile")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="view_statistics")],
        [InlineKeyboardButton(text="🏆 Достижения", callback_data="view_achievements")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ]
)

# Simple back keyboard
back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_menu")],
    ]
)