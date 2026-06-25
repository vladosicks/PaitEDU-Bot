from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.coursework_menu import coursework_menu

router = Router()


@router.callback_query(F.data == "service_coursework")
async def coursework_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🎓 Курсові роботи</b>\n\n"

        "✅ Виконуємо курсові роботи будь-якої складності.\n\n"

        "📚 Гуманітарні\n"
        "💻 Технічні\n"
        "📊 Економічні\n"
        "⚖️ Юридичні\n\n"

        "⏳ Термін виконання:\n"
        "від 2 днів.",

        parse_mode="HTML",
        reply_markup=coursework_menu
    )