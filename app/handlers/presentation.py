from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.presentation_menu import presentation_menu

router = Router()


@router.callback_query(F.data == "service_presentation")
async def presentation_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📊 Презентації</b>\n\n"

        "✅ Створюємо сучасні та стильні презентації.\n\n"

        "🎨 Індивідуальний дизайн\n"
        "📈 Інфографіка\n"
        "📊 Діаграми та схеми\n"
        "🖼️ Якісні ілюстрації\n\n"

        "⏳ Термін виконання:\n"
        "від 1 дня.",

        parse_mode="HTML",
        reply_markup=presentation_menu
    )