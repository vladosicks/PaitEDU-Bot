from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.crud import get_orders_by_user
from app.keyboards.cabinet_menu import cabinet_menu

router = Router()


@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    orders = get_orders_by_user(callback.from_user.id)

    active_orders = [
        order for order in orders
        if order.status in ["new", "work"]
    ]

    completed_orders = [
        order for order in orders
        if order.status in ["done", "archive"]
    ]

    await callback.message.edit_text(
        f"💙 <b>PaitEDU</b>\n"
        f"────────────────\n\n"

        f"👤 <b>Особистий кабінет</b>\n\n"

        f"Вітаємо, <b>{callback.from_user.first_name}</b>! 👋\n\n"

        f"📦 Активних замовлень: <b>{len(active_orders)}</b>\n"
        f"✅ Виконано: <b>{len(completed_orders)}</b>\n\n"

        f"👇 Оберіть потрібну дію.",

        parse_mode="HTML",
        reply_markup=cabinet_menu
    )

    await callback.answer()