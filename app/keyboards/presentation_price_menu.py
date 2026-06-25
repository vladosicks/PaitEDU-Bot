from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

presentation_price_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="presentation_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="service_presentation"
            )
        ]
    ]
)