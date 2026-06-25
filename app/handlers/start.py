from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        text="👋 Вітаємо у PaitEDU!\n\nОберіть потрібний розділ:",
        reply_markup=main_menu
    )

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        text="👋 Вітаємо у PaitEDU!\n\nОберіть потрібний розділ:",
        reply_markup=main_menu
    )