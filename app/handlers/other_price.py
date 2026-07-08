from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.other_price_menu import other_price_menu

router = Router()


@router.callback_query(F.data == "other_price")
async def other_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "<b>📚 Інші завдання</b>\n\n"

        "Ми також допомагаємо з:\n\n"

        "📊 Лабораторними роботами\n"
        "📝 Практичними роботами\n"
        "📄 Контрольними роботами\n"
        "📚 Звітами з практики\n"
        "💻 Програмуванням\n"
        "📈 Таблицями Excel\n"
        "📂 Іншими індивідуальними завданнями\n\n"

        "💰 <b>Вартість визначається індивідуально.</b>\n\n"

        "На ціну можуть впливати:\n"
        "📖 складність завдання;\n"
        "⏳ термін виконання;\n"
        "📑 обсяг роботи;\n"
        "💡 особливі вимоги викладача.\n\n"

        "💬 Надішліть умову завдання — швидко розрахуємо точну вартість.",

        parse_mode="HTML",
        reply_markup=other_price_menu
    )