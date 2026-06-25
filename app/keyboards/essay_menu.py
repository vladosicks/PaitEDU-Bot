from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

essay_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Дізнатись ціну",
                callback_data="essay_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="essay_order"
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