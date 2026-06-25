from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.presentation_price_menu import presentation_price_menu

router = Router()


@router.callback_query(F.data == "presentation_price")
async def presentation_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>💰 Вартість презентацій</b>\n\n"

        "📊 До 10 слайдів — <b>від 300 грн</b>\n"
        "📊 До 20 слайдів — <b>від 500 грн</b>\n"
        "📊 До 30 слайдів — <b>від 700 грн</b>\n\n"

        "✨ <b>Кожна презентація оцінюється індивідуально.</b>\n\n"

        "На вартість можуть впливати:\n"
        "🎨 унікальний дизайн;\n"
        "📈 інфографіка та діаграми;\n"
        "🖼 пошук і обробка зображень;\n"
        "🎬 анімації та ефекти;\n"
        "⏰ термінове виконання.\n\n"

        "💬 Надішліть завдання — ми швидко розрахуємо точну вартість.",

        parse_mode="HTML",
        reply_markup=presentation_price_menu
    )