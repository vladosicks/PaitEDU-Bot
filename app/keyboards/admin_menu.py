from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📋 Замовлення",
                callback_data="admin_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data="admin_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Пошук",
                callback_data="admin_search"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Налаштування",
                callback_data="admin_settings"
            )
        ]
    ]
)