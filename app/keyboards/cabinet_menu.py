from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cabinet_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📦 Мої замовлення",
                callback_data="my_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Зв'язок з менеджером",
                callback_data="contact_manager"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 Головне меню",
                callback_data="back_main"
            )
        ]
    ]
)