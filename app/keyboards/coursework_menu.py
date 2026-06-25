from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

coursework_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Дізнатись ціну",
                callback_data="coursework_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="coursework_order"
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