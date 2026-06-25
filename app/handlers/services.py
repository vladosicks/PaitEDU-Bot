from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram import F
from app.keyboards.services_menu import services_menu

router = Router()
@router.callback_query(F.data == "menu_services")
async def services_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 Оберіть потрібну послугу:",
        reply_markup=services_menu
    )

@router.callback_query(F.data == "back_services")
async def back_services(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 Оберіть потрібну послугу:",
        reply_markup=services_menu
    )