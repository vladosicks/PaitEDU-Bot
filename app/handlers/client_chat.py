from aiogram import Router
from aiogram.types import Message

from app.database.crud import (
    get_message_by_telegram_id,
    get_order_by_id,
    add_message
)
from app.config.settings import ADMIN_ID

router = Router()


@router.message()
async def client_reply(message: Message):

    if not message.reply_to_message:
        return

    db_message = get_message_by_telegram_id(
        message.reply_to_message.message_id
    )

    if not db_message:
        return

    order = get_order_by_id(db_message.order_id)

    if not order:
        return

    add_message(
        order_id=order.id,
        sender="client",
        text=message.text or "",
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