from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.diploma_price_menu import diploma_price_menu

router = Router()


@router.callback_query(F.data == "diploma_price")
async def diploma_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>💰 Вартість дипломних робіт</b>\n\n"

        "📄 До 40 сторінок — <b>від 2500 грн</b>\n"
        "📄 До 60 сторінок — <b>від 3500 грн</b>\n"
        "📄 Понад 60 сторінок — <b>ціна договірна</b>\n\n"

        "⭐ Якщо робота термінова або має особливі вимоги — "
        "вартість узгоджується індивідуально.",

        parse_mode="HTML",
        reply_markup=diploma_price_menu
    )