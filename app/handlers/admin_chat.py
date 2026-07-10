from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.keyboards.client_reply_menu import client_reply_menu
from app.states.order_state import OrderState
from app.database.crud import (
    get_order_by_id,
    add_message,
    set_chat_active
)

router = Router()


@router.callback_query(F.data.startswith("reply_"))
async def reply_to_user(callback: CallbackQuery, state: FSMContext):

    order_id = int(callback.data.split("_")[1])

    await state.update_data(order_id=order_id)

    set_chat_active(order_id, 1)

    await state.set_state(OrderState.waiting_admin_reply)

    await callback.message.answer(
        "💬 Введіть повідомлення, яке потрібно надіслати клієнту."
    )

    await callback.answer()


@router.message(OrderState.waiting_admin_reply)
async def send_reply(message: Message, state: FSMContext):

    data = await state.get_data()

    order = get_order_by_id(data["order_id"])

    if not order:
        await message.answer("❌ Замовлення не знайдено.")
        await state.clear()
        return

    sent = await message.bot.send_message(
        chat_id=order.user_id,
        text=(
            f"💬 <b>Нове повідомлення щодо замовлення №{order.id}</b>\n\n"
            f"{message.text}"
        ),
        parse_mode="HTML",
        reply_markup=client_reply_menu(order.id)
    )

    add_message(
        order_id=order.id,
        sender="admin",
        text=message.text,
        telegram_message_id=sent.message_id
    )

    await state.clear()

    await message.answer(
        "✅ Повідомлення успішно відправлено клієнту."
    )