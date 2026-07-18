from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_ready_menu(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написати менеджеру",
                    callback_data=f"contact_manager_{order_id}"
                )
            ]
        ]
    )