from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

coursework_price_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="coursework_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="service_coursework"
            )
        ]
    ]
)