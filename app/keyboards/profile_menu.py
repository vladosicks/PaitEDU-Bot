from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.ui.buttons import HOME


def profile_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Мої замовлення",
                    callback_data="my_orders"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Підтримка",
                    callback_data="support"
                )
            ],
            [
                InlineKeyboardButton(
                    text=HOME,
                    callback_data="home"
                )
            ]
        ]
    )