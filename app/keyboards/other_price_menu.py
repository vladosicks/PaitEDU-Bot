from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

other_price_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="other_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅ Назад",
                callback_data="service_other"
            )
        ]
    ]
)