from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

how_to_use_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_main"
            )
        ]
    ]
)