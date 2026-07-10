from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime

from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)
    username = Column(String)
    full_name = Column(String)

    service = Column(String)

    description = Column(Text)

    status = Column(String, default="new")

    chat_active = Column(Integer, default=0)

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