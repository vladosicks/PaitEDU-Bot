from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_orders_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🟢 Нові",
                callback_data="orders_new"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟡 В роботі",
                callback_data="orders_work"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Виконані",
                callback_data="orders_done"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 Архів",
                callback_data="orders_archive"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_back"
            )
        ]
    ]
)

