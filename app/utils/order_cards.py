from app.utils.statuses import STATUS_NAMES, PAYMENT_NAMES


def build_admin_order_text(order, history):

    price = (
        f"{order.price} грн"
        if order.price
        else "Не встановлена"
    )

    deadline = (
        order.deadline.strftime("%d.%m.%Y")
        if order.deadline
        else "Не встановлений"
    )

    status = STATUS_NAMES.get(
        order.status,
        order.status
    )

    payment = PAYMENT_NAMES.get(
        order.payment_status,
        order.payment_status
    )

    return (
        f"📄 <b>Замовлення #{order.id}</b>\n\n"

        f"👤 <b>Клієнт:</b> {order.full_name}\n"
        f"🆔 <b>ID:</b> <code>{order.user_id}</code>\n"
        f"📨 <b>Username:</b> @{order.username or 'немає'}\n\n"

        f"📚 <b>Послуга:</b> {order.service}\n"

        f"💰 <b>Вартість:</b> {price}\n"

        f"📅 <b>Дедлайн:</b> {deadline}\n"

        f"📌 <b>Статус:</b> {status}\n"

        f"💳 <b>Оплата:</b> {payment}\n\n"

        f"📝 <b>Опис:</b>\n"
        f"{order.description or '—'}\n\n"

        f"━━━━━━━━━━━━━━━━━━\n"

        f"<b>💬 Історія листування</b>\n\n"

        f"{history}"
    )