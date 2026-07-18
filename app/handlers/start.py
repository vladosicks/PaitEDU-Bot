from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.keyboards.how_to_use_menu import how_to_use_menu

import re

from app.keyboards.tutorial_menu import tutorial_menu
from app.ui.progress import progress

from app.ui.cards import welcome_card_v2
from app.config.settings import ADMIN_ID
from app.ui.tutorial import TUTORIAL_PAGES

from app.keyboards.start_menu import start_menu
from app.keyboards.main_menu import main_menu
from app.handlers.admin import open_admin_panel



router = Router()


@router.message(CommandStart())
async def start_command(message: Message):

    await message.answer(
        welcome_card_v2(),
        parse_mode="HTML",
        reply_markup=start_menu
    )

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):

    await callback.message.edit_text(
        welcome_card_v2(),
        parse_mode="HTML",
        reply_markup=start_menu
    )

@router.callback_query(F.data == "how_to_use")
async def tutorial_start(callback: CallbackQuery):

    await callback.message.edit_text(
        text=TUTORIAL_PAGES[1],
        parse_mode="HTML",
        reply_markup=tutorial_menu(1)
    )

    await callback.answer()


@router.callback_query(F.data.regexp(r"^tutorial_(\d+)$"))
async def tutorial_pages(callback: CallbackQuery):

    page = int(callback.data.split("_")[1])

    await callback.message.edit_text(
        text=TUTORIAL_PAGES[page],
        parse_mode="HTML",
        reply_markup=tutorial_menu(page)
    )

    await callback.answer()

@router.callback_query(F.data == "admin_panel")
async def open_admin(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:

        await callback.answer(
            "⛔ У вас немає доступу.",
            show_alert=True
        )
        return

    await open_admin_panel(callback)