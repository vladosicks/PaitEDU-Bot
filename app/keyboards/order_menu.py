from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


order_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Скасувати",
                callback_data="order_cancel"
            )
        ]
    ]
)