from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def client_reply_menu(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Відповісти",
                    callback_data=f"client_reply_{order_id}"
                )
            ]
        ]
    )