from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.ui.buttons import (
    PREVIOUS,
    NEXT,
    START,
    HOME
)


def tutorial_menu(page: int):

    keyboard = []

    buttons = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text=PREVIOUS,
                callback_data=f"tutorial_{page - 1}"
            )
        )

    if page < 5:
        buttons.append(
            InlineKeyboardButton(
                text=NEXT,
                callback_data=f"tutorial_{page + 1}"
            )
        )
    else:
        buttons.append(
            InlineKeyboardButton(
                text=START,
                callback_data="menu_services"
            )
        )

    keyboard.append(buttons)

    keyboard.append(
        [
            InlineKeyboardButton(
                text=HOME,
                callback_data="back_main"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )