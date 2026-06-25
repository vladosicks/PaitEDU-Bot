from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

diploma_price_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📄 Замовити",
                callback_data="diploma_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="service_diploma"
            )
        ]
    ]
)