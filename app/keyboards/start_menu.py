from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.ui.buttons import START, PROFILE, ADMIN


start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=START,
                callback_data="menu_services"
            )
        ],
        [
            InlineKeyboardButton(
                text=PROFILE,
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                text="📖 Як користуватись",
                callback_data="how_to_use"
            )
        ],
        [
            InlineKeyboardButton(
                text=ADMIN,
                callback_data="admin_panel"
            )
        ]
    ]
)