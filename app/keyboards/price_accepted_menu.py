from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def price_accepted_menu(order_id: int):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📂 Відкрити замовлення",
                    callback_data=f"open_order_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟡 Розпочати виконання",
                    callback_data=f"start_work_{order_id}"
                )
            ]
        ]
    )