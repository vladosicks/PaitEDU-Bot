from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message
)
from aiogram.fsm.context import FSMContext

from app.states.order_state import OrderState

from app.database.crud import (
    update_price_status,
    get_order_by_id,
    update_order_status,
    update_order_price,
    clear_pending_price
)

from app.utils.constants import *

from app.config.settings import ADMIN_ID

from app.keyboards.price_confirm_menu import price_confirm_menu
from app.keyboards.price_discussion_menu import price_discussion_menu
from app.keyboards.price_accepted_menu import price_accepted_menu
from app.database.crud import clear_pending_price

router = Router()


@router.callback_query(F.data.startswith("price_accept_"))
async def accept_price(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    update_price_status(
        order_id,
        PRICE_ACCEPTED
    )

    order = get_order_by_id(order_id)

    update_order_price(
    order_id,
    order.pending_price
    )

    clear_pending_price(order_id)

    order = get_order_by_id(order_id)

    await callback.bot.send_message(
        ADMIN_ID,
        (
            "✅ <b>Клієнт погодив вартість</b>\n\n"
            f"📄 Замовлення №<b>{order.id}</b>\n"
            f"💰 <b>{order.price} грн</b>\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "Наступний крок:\n"
            "🟡 Розпочати виконання роботи."
        ),
        parse_mode="HTML",
        reply_markup=price_accepted_menu(order.id)
    )

    await callback.message.edit_text(
        "✅ <b>Вартість погоджено.</b>\n\n"
        "🟡 Ваше замовлення прийнято в роботу.\n\n"
        "Наш спеціаліст уже розпочав виконання.\n"
        "Ми повідомимо вас, щойно робота буде готова.",
        parse_mode="HTML"
    )

    await callback.answer()

@router.callback_query(F.data.startswith("price_decline_"))
async def decline_price(callback: CallbackQuery, state: FSMContext):

    order_id = int(callback.data.split("_")[2])
    clear_pending_price(order_id)

    await state.update_data(order_id=order_id)

    await state.set_state(
        OrderState.waiting_price_decline
    )

    await callback.message.edit_text(
        "💬 <b>Обговорення вартості</b>\n\n"
        "Напишіть:\n\n"
        "• яка ціна для вас комфортна;\n"
        "або\n"
        "• що саме вас не влаштовує.\n\n"
        "Менеджер обов'язково перегляне повідомлення.",
        parse_mode="HTML"
    )

    await callback.answer()

@router.message(OrderState.waiting_price_decline)
async def process_price_decline(message: Message, state: FSMContext):

    data = await state.get_data()

    order_id = data["order_id"]

    order = get_order_by_id(order_id)

    update_price_status(
        order_id,
        PRICE_DECLINED
    )

    await message.bot.send_message(
        ADMIN_ID,
        (
            "💬 <b>Обговорення вартості</b>\n\n"

            f"👤 <b>{order.full_name}</b>\n\n"

            f"📄 Замовлення №<b>{order.id}</b>\n"

            f"💰 Поточна ціна: <b>{order.price} грн</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "<b>Повідомлення клієнта:</b>\n\n"

            f"{message.text}"
        ),
        parse_mode="HTML",
        reply_markup=price_discussion_menu(order.id)
    )

    await message.answer(
        "✅ Ваше повідомлення передано менеджеру.\n\n"
        "Ми переглянемо його та запропонуємо нову вартість або зв'яжемося з вами."
    )

    await state.clear()