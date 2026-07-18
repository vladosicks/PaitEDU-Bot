from app.database.database import SessionLocal
from app.database.models import Order, Message

from app.utils.constants import (
    STATUS_NEW,
    STATUS_WORK,
    STATUS_DONE,
    STATUS_ARCHIVE
)

def add_order(
    user_id,
    username,
    full_name,
    service,
    description
):
    db = SessionLocal()

    order = Order(
        user_id=user_id,
        username=username,
        full_name=full_name,
        service=service,
        description=description
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    db.close()

    return order


def get_order_by_id(order_id):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    db.close()

    return order


def get_new_orders():
    db = SessionLocal()

    orders = (
        db.query(Order)
        .filter(Order.status == STATUS_NEW)
        .order_by(Order.created_at.desc())
        .all()
    )

    db.close()

    return orders


def get_work_orders():
    db = SessionLocal()

    orders = (
        db.query(Order)
        .filter(Order.status == STATUS_WORK)
        .order_by(Order.created_at.desc())
        .all()
    )

    db.close()

    return orders


def get_done_orders():
    db = SessionLocal()

    orders = (
        db.query(Order)
        .filter(Order.status == STATUS_DONE)
        .order_by(Order.created_at.desc())
        .all()
    )

    db.close()

    return orders


def update_order_status(order_id, status):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        order.status = status
        db.commit()

    db.close()


def add_message(
    order_id,
    sender,
    text,
    telegram_message_id=None
):
    db = SessionLocal()

    message = Message(
        order_id=order_id,
        sender=sender,
        text=text,
        telegram_message_id=telegram_message_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    db.close()

    return message

def get_messages(order_id):
    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(Message.order_id == order_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    db.close()

    return messages


def get_message_by_telegram_id(message_id):
    db = SessionLocal()

    message = (
        db.query(Message)
        .filter(Message.telegram_message_id == message_id)
        .first()
    )

    db.close()

    return message


def mark_messages_read(order_id):
    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(
            Message.order_id == order_id,
            Message.sender == "client",
            Message.is_read == 0
        )
        .all()
    )

    for message in messages:
        message.is_read = 1

    db.commit()
    db.close()


def get_unread_messages(order_id):
    db = SessionLocal()

    messages = (
        db.query(Message)
        .filter(
            Message.order_id == order_id,
            Message.sender == "client",
            Message.is_read == 0
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    db.close()

    return messages


def delete_order(order_id):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        db.delete(order)
        db.commit()

    db.close()


def delete_messages(order_id):
    db = SessionLocal()

    (
        db.query(Message)
        .filter(Message.order_id == order_id)
        .delete()
    )

    db.commit()
    db.close()


def get_orders_count():
    db = SessionLocal()

    count = db.query(Order).count()

    db.close()

    return count


def get_orders_by_user(user_id):
    db = SessionLocal()

    orders = (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )

    db.close()

    return orders

def set_chat_active(order_id, active):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        order.chat_active = active
        db.commit()

    db.close()


def get_active_order_by_user(user_id):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(
            Order.user_id == user_id,
            Order.chat_active == 1
        )
        .first()
    )

    db.close()

    return order

def get_archive_orders():
    db = SessionLocal()

    orders = (
        db.query(Order)
        .filter(Order.status == STATUS_ARCHIVE)
        .order_by(Order.created_at.desc())
        .all()
    )

    db.close()

    return orders

def search_orders(query):
    db = SessionLocal()

    search = query.strip().replace("#", "").replace("@", "")

    orders = []

    # Пошук по імені та username
    found = (
        db.query(Order)
        .filter(
            (Order.full_name.ilike(f"%{search}%")) |
            (Order.username.ilike(f"%{search}%"))
        )
        .all()
    )

    orders.extend(found)

    # Якщо введено число
    if search.isdigit():

        # Пошук по номеру замовлення
        order = (
            db.query(Order)
            .filter(Order.id == int(search))
            .first()
        )

        if order and order not in orders:
            orders.append(order)

        # Пошук по Telegram ID
        user_orders = (
            db.query(Order)
            .filter(Order.user_id == int(search))
            .all()
        )

        for order in user_orders:
            if order not in orders:
                orders.append(order)

    db.close()

    return orders

def get_orders_count_by_status(status):
    db = SessionLocal()

    count = (
        db.query(Order)
        .filter(Order.status == status)
        .count()
    )

    db.close()

    return count

def update_order_price(order_id: int, price: int):

    db = SessionLocal()

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if order:

        order.price = price

        db.commit()

    db.close()

def update_pending_price(order_id: int, price: int):

    with SessionLocal() as session:

        order = session.get(Order, order_id)

        if not order:
            return

        order.pending_price = price

        session.commit()


def clear_pending_price(order_id: int):

    with SessionLocal() as session:

        order = session.get(Order, order_id)

        if not order:
            return

        order.pending_price = None

        session.commit()

def update_price_status(order_id: int, status: str):

    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        order.price_status = status
        db.commit()

    db.close()

def update_order_document(
    order_id: int,
    file_id: str,
    file_name: str
):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        order.document_file_id = file_id
        order.document_name = file_name
        db.commit()

    db.close()

def update_payment_status(
    order_id: int,
    payment_status: str
):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        order.payment_status = payment_status
        db.commit()

    db.close()

def update_payment_status(
    order_id: int,
    status: str
):
    db = SessionLocal()

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if order:
        order.payment_status = status
        db.commit()

    db.close()