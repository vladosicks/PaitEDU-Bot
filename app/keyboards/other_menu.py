from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

other_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Дізнатись ціну",
                callback_data="other_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="other_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅ Назад",
                callback_data="back_services"
            )
        ]
    ]
)