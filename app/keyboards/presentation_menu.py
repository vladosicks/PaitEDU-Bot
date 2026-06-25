from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

presentation_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Дізнатись ціну",
                callback_data="presentation_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="presentation_order"
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