from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_order_menu(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Прийняти",
                    callback_data=f"accept_{user_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Відхилити",
                    callback_data=f"decline_{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Написати клієнту",
                    callback_data=f"reply_{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏁 Замовлення виконано",
                    callback_data=f"done_{user_id}"
                )
            ]
        ]
    )