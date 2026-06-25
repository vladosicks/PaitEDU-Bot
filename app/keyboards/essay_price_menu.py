from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

essay_price_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="essay_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="service_essay"
            )
        ]
    ]
)