from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.essay_price_menu import essay_price_menu

router = Router()


@router.callback_query(F.data == "essay_price")
async def essay_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>💰 Вартість рефератів</b>\n\n"

        "📄 До 10 сторінок — <b>300 грн</b>\n"
        "📄 До 20 сторінок — <b>500 грн</b>\n"
        "📄 До 30 сторінок — <b>700 грн</b>\n\n"

        "⭐ Якщо робота термінова або має особливі вимоги — "
        "вартість узгоджується індивідуально.",

        parse_mode="HTML",
        reply_markup=essay_price_menu
    )