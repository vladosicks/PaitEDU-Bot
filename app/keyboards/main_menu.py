from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.ui.buttons import START, PROFILE, ADMIN

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📚 Послуги",
                callback_data="menu_services"
            )
        ],
        [
            InlineKeyboardButton(
                text=PROFILE,
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                text="💰 Прайс",
                callback_data="menu_price"
            )
        ],
        [
            InlineKeyboardButton(
                text="📂 Приклади робіт",
                callback_data="menu_examples"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Залишити замовлення",
                callback_data="menu_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="❓ FAQ",
                callback_data="menu_faq"
            )
        ],
        [
            InlineKeyboardButton(
                text="👨‍💻 Зв'язатися",
                callback_data="menu_contact"
            )
        ]
    ]
)