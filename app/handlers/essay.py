from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.essay_menu import essay_menu

router = Router()


@router.callback_query(F.data == "service_essay")
async def essay_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📄 <b>Реферати</b>\n\n"
        "✅ Виконуємо реферати будь-якої складності.\n\n"
        "📚 Гуманітарні\n"
        "💻 Технічні\n"
        "💼 Економічні\n\n"
        "⏳ Термін виконання:\n"
        "від 1 дня.",
        parse_mode="HTML",
        reply_markup=essay_menu
    )