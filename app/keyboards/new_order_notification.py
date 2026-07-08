from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def new_order_notification(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👀 Відкрити в CRM",
                    callback_data=f"open_order_{order_id}"
                )
            ]
        ]
    )