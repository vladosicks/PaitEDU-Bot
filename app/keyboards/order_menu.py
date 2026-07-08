from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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