from aiogram import Router
from aiogram.types import Message

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.keyboards.message_card_menu import message_card_menu

from app.states.order_state import OrderState

from app.database.crud import (
    get_message_by_telegram_id,
    get_order_by_id,
    add_message
)
from app.config.settings import ADMIN_ID


router = Router()

@router.callback_query(F.data.startswith("client_reply_"))
async def start_client_reply(callback: CallbackQuery, state: FSMContext):

    order_id = int(callback.data.split("_")[2])

    await state.update_data(order_id=order_id)

    await state.set_state(OrderState.waiting_client_reply)

    await callback.message.answer(
        "✍️ Напишіть повідомлення менеджеру."
    )

    await callback.answer()


@router.message(OrderState.waiting_client_reply)
async def send_client_reply(message: Message, state: FSMContext):

    data = await state.get_data()

    order = get_order_by_id(data["order_id"])

    if not order:
        await message.answer("❌ Замовлення не знайдено.")
        await state.clear()
        return

    add_message(
        order_id=order.id,
        sender="client",
        text=message.text,
        telegram_message_id=message.message_id
    )

    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"💬 <b>Нова відповідь від клієнта</b>\n\n"
            f"📄 Замовлення №{order.id}\n"
            f"👤 {order.full_name}\n\n"
            f"{message.text}"
        ),
        parse_mode="HTML"
    )

    await message.answer(
        "✅ Повідомлення успішно відправлено менеджеру."
    )

    await state.clear()

@router.callback_query(F.data.startswith("contact_manager_"))
async def contact_manager(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    order = get_order_by_id(order_id)

    username = (
        f"@{order.username}"
        if order.username
        else "немає"
    )
    await callback.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🔔 <b>Клієнт готовий до оплати</b>\n\n"
            f"📄 Замовлення №<b>{order.id}</b>\n"
            f"💰 Сума: <b>{order.price} грн</b>\n\n"
            f"👤 {order.full_name}\n"
            f"📱 {username}\n"
            f"🆔 <code>{order.user_id}</code>"
        ),
        parse_mode="HTML",
        reply_markup=message_card_menu(order.id)
     )
     
    await callback.answer(
        "✅ Менеджера повідомлено."
    )

    await callback.message.answer(
        "✅ Запит успішно відправлено.\n\n"
        "Менеджер зв'яжеться з вами найближчим часом."
    )