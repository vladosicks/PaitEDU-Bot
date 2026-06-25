from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

translation_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💰 Дізнатись ціну",
                callback_data="translation_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="translation_order"
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