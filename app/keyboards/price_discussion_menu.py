from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def price_discussion_menu(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Запропонувати нову ціну",
                    callback_data=f"set_price_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Написати клієнту",
                    callback_data=f"reply_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📂 Відкрити замовлення",
                    callback_data=f"open_order_{order_id}"
                )
            ]
        ]
    )