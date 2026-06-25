from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.translation_price_menu import translation_price_menu

router = Router()


@router.callback_query(F.data == "translation_price")
async def translation_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>🌍 Вартість перекладів</b>\n\n"

        "🇬🇧 Англійська\n"
        "🇩🇪 Німецька\n"
        "🇵🇱 Польська\n"
        "🇪🇸 Іспанська\n"
        "🇫🇷 Французька\n\n"

        "💰 <b>Вартість визначається індивідуально.</b>\n\n"

        "На ціну можуть впливати:\n"
        "📄 обсяг тексту;\n"
        "📚 складність тематики;\n"
        "⚖️ юридичний, медичний або технічний текст;\n"
        "⏰ терміновість виконання;\n"
        "✍️ необхідність редагування або оформлення.\n\n"

        "💬 Надішліть текст або файл — ми швидко розрахуємо точну вартість.",

        parse_mode="HTML",
        reply_markup=translation_price_menu
    )