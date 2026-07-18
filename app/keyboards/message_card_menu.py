from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def message_card_menu(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
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