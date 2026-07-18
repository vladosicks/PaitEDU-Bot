from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.constants import *


def order_card_menu(
    order_id: int,
    status: str,
    price_status: str = PRICE_WAITING
):

    keyboard = []

    # -------------------------
    # Нове замовлення
    # -------------------------

    if status == STATUS_NEW:

        # Ціна ще не погоджена
        if price_status != PRICE_ACCEPTED:

            keyboard.append(
                [
                    InlineKeyboardButton(
                        text="💰 Встановити ціну",
                        callback_data=f"set_price_{order_id}"
                    )
                ]
            )

        # Клієнт погодив ціну
        else:

            keyboard.append(
                [
                    InlineKeyboardButton(
                        text="🟡 Розпочати виконання",
                        callback_data=f"start_work_{order_id}"
                    )
                ]
            )

    # -------------------------
    # В роботі
    # -------------------------

    elif status == STATUS_WORK:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text="📄 Робота готова",
                    callback_data=f"order_done_{order_id}"
                )
            ]
        )

    # -------------------------
    # Готово
    # -------------------------
    elif status == STATUS_DONE:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text="📎 Завантажити файл",
                    callback_data=f"upload_file_{order_id}"
                )
            ]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text="💳 Підтвердити оплату",
                    callback_data=f"confirm_payment_{order_id}"
                )
            ]
        )

    # -------------------------
    # Чат
    # -------------------------

    keyboard.append(
        [
            InlineKeyboardButton(
                text="💬 Написати клієнту",
                callback_data=f"reply_{order_id}"
            )
        ]
    )

    # -------------------------
    # Повернути
    # -------------------------

    if status in [STATUS_DONE, STATUS_ARCHIVE]:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text="🔄 Повернути в роботу",
                    callback_data=f"order_return_{order_id}"
                )
            ]
        )

    # -------------------------
    # Назад
    # -------------------------

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