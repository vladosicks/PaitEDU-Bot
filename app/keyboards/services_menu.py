from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

services_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📄 Реферати", callback_data="service_essay")],
        [InlineKeyboardButton(text="📚 Курсові", callback_data="service_coursework")],
        [InlineKeyboardButton(text="🎓 Дипломні", callback_data="service_diploma")],
        [InlineKeyboardButton(text="🌍 Переклади", callback_data="service_translation")],
        [InlineKeyboardButton(text="📊 Презентації", callback_data="service_presentation")],
        [InlineKeyboardButton(text="📦 Інші завдання", callback_data="service_other")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")]
    ]
)