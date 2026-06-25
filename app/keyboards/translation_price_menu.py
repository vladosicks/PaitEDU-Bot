from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

translation_price_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Замовити",
                callback_data="translation_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="service_translation"
            )
        ]
    ]
)