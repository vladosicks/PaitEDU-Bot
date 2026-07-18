from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.utils.constants import *

from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Клієнт
    user_id = Column(Integer)
    username = Column(String)
    full_name = Column(String)

    # Замовлення
    service = Column(String)
    description = Column(Text)

    # Вартість
    price = Column(Integer, nullable=True)

    pending_price = Column(
        Integer,
        nullable=True
    )   

    # Статус виконання
    status = Column(String, default=STATUS_NEW)

    # Статус оплати
    payment_status = Column(String, default=PAYMENT_WAITING)

    # Статус погодження вартості
    price_status = Column(
        String,
        default=PRICE_WAITING
    )

    # Готовий файл
    document_file_id = Column(String, nullable=True)
    document_name = Column(String, nullable=True)

    # Коментар менеджера (не бачить клієнт)
    manager_comment = Column(Text, nullable=True)

    # Дедлайн
    deadline = Column(DateTime, nullable=True)

    # Чат
    chat_active = Column(Integer, default=0)

    # Дата створення
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    sender = Column(
        String,
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    telegram_message_id = Column(
        Integer,
        nullable=True
    )

    is_read = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )