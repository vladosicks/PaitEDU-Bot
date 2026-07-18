from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def price_confirm_menu(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Погоджуюсь",
                    callback_data=f"price_accept_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Обговорити ціну",
                    callback_data=f"price_decline_{order_id}"
                )
            ]
        ]
    )