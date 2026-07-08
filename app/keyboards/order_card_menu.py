from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def order_card_menu(order_id: int, status: str):

    keyboard = []

    if status == "new":
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="🟡 Взяти в роботу",
                    callback_data=f"order_work_{order_id}"
                )
            ]
        )

    elif status == "work":
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="✅ Виконано",
                    callback_data=f"order_done_{order_id}"
                )
            ]
        )

    elif status == "done":
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="🔄 Повернути в роботу",
                    callback_data=f"order_return_{order_id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="💬 Написати клієнту",
                callback_data=f"reply_{order_id}"
            )
        ]
    )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"orders_{status}"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )