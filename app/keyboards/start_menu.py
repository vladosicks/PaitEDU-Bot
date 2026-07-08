from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 Почати",
                callback_data="menu_services"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔐 Адмін-панель",
                callback_data="admin_panel"
            )
        ]
    ]
)