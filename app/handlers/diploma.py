from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.diploma_menu import diploma_menu

router = Router()


@router.callback_query(F.data == "service_diploma")
async def diploma_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📜 Дипломні роботи</b>\n\n"

        "✅ Допомагаємо з дипломними роботами будь-якої складності.\n\n"

        "📚 Гуманітарні\n"
        "💻 Технічні\n"
        "📊 Економічні\n"
        "⚖️ Юридичні\n\n"

        "⏳ Термін виконання:\n"
        "від 15 днів.",

        parse_mode="HTML",
        reply_markup=diploma_menu
    )