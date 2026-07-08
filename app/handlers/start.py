from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.config.settings import ADMIN_ID

from app.keyboards.start_menu import start_menu
from app.keyboards.main_menu import main_menu

from app.handlers.admin import open_admin_panel


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):

    await message.answer(
        "👋 <b>Ласкаво просимо до PaitEDU!</b>\n\n"
        "📚 Ми допомагаємо з:\n"
        "• Рефератами\n"
        "• Курсовими роботами\n"
        "• Дипломними роботами\n"
        "• Презентаціями\n"
        "• Перекладами\n\n"
        "⬇️ Оберіть потрібний розділ:",
        parse_mode="HTML",
        reply_markup=start_menu
    )


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):

    await callback.message.edit_text(
        "👋 <b>Ласкаво просимо до PaitEDU!</b>\n\n"
        "📚 Ми допомагаємо з:\n"
        "• Рефератами\n"
        "• Курсовими роботами\n"
        "• Дипломними роботами\n"
        "• Презентаціями\n"
        "• Перекладами\n\n"
        "⬇️ Оберіть потрібний розділ:",
        parse_mode="HTML",
        reply_markup=start_menu
    )


@router.callback_query(F.data == "admin_panel")
async def open_admin(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:

        await callback.answer(
            "⛔ У вас немає доступу.",
            show_alert=True
        )
        return

    await open_admin_panel(callback)