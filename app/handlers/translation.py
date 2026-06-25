from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.translation_menu import translation_menu

router = Router()


@router.callback_query(F.data == "service_translation")
async def translation_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🌐 Переклади</b>\n\n"

        "✅ Виконуємо професійні письмові переклади.\n\n"

        "🇺🇦 Українська\n"
        "🇬🇧 Англійська\n"
        "🇩🇪 Німецька\n"
        "🇪🇸 Іспанська\n\n"

        "⏳ Термін виконання:\n"
        "від 1 дня.",

        parse_mode="HTML",
        reply_markup=translation_menu
    )