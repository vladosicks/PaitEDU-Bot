from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.essay_menu import essay_menu

router = Router()


@router.callback_query(F.data == "service_other")
async def other_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📋 Інші завдання</b>\n\n"

        "✅ Виконуємо різноманітні навчальні завдання.\n\n"

        "📌 Контрольні\n"
        "📝 Самостійні роботи\n"
        "🧪 Лабораторне завдання\n"
        "📊 Практичні роботи\n"
        "💻 Індивідуальні завдання\n\n"

        "⏳ Термін виконання:\n"
        "від 1 дня.",

        parse_mode="HTML",
        reply_markup=essay_menu
    )