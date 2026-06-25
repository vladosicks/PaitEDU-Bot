from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.coursework_price_menu import coursework_price_menu

router = Router()


@router.callback_query(F.data == "coursework_price")
async def coursework_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>💰 Вартість курсових робіт</b>\n\n"

        "📄 До 25 сторінок — <b>900 грн</b>\n"
        "📄 До 35 сторінок — <b>1200 грн</b>\n"
        "📄 До 50 сторінок — <b>1600 грн</b>\n\n"

        "⭐ Якщо робота термінова або має особливі вимоги — "
        "вартість узгоджується індивідуально.",

        parse_mode="HTML",
        reply_markup=coursework_price_menu
    )