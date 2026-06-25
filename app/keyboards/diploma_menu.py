from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

diploma_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Дізнатись ціну",
                callback_data="diploma_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📄 Замовити",
                callback_data="diploma_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_services"
            )
        ]
    ]
)