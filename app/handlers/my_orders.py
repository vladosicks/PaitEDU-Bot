from aiogram import Router, F

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message
)

from aiogram.fsm.context import FSMContext
from app.database.crud import get_orders_by_user
from app.keyboards.cabinet_menu import cabinet_menu
from app.keyboards.message_card_menu import message_card_menu
from datetime import datetime
from app.ui.progress import build_progress
from app.ui.cards import order_card

from app.states.order_state import OrderState

from app.config.settings import ADMIN_ID

from app.database.crud import (
    get_order_by_id,
    add_message
)

router = Router()


@router.callback_query(F.data == "my_orders")
async def my_orders(callback: CallbackQuery):

    orders = get_orders_by_user(callback.from_user.id)

    if not orders:
        await callback.message.edit_text(
            "💙 <b>PaitEDU</b>\n"
            "────────────────\n\n"

            "📦 <b>Мої замовлення</b>\n\n"

            "У вас поки що немає замовлень.",

            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🏠 Головне меню",
                            callback_data="back_main"
                        )
                    ]
                ]
            )
        )

        await callback.answer()
        return

    status_icons = {
        "new": "🟢",
        "waiting_payment": "💳",
        "paid": "💵",
        "work": "🟡",
        "review": "🔍",
        "done": "✅",
        "archive": "📦"
    }

    keyboard = []

    for order in orders:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{status_icons.get(order.status, '❓')} №{order.id} • {order.service}",
                    callback_data=f"client_order_{order.id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🏠 Головне меню",
                callback_data="back_main"
            )
        ]
    )

    await callback.message.edit_text(
        "💙 <b>PaitEDU</b>\n"
        "────────────────\n\n"

        "📦 <b>Мої замовлення</b>\n\n"

        f"Усього замовлень: <b>{len(orders)}</b>\n\n"

        "👇 Оберіть замовлення",

        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()

@router.callback_query(F.data == "completed_orders")
async def completed_orders(callback: CallbackQuery):

    orders = get_orders_by_user(callback.from_user.id)

    completed = [
        order for order in orders
        if order.status in ["done", "archive"]
    ]

    if not completed:
        await callback.message.edit_text(
            "✅ <b>Виконані роботи</b>\n\n"
            "У вас поки немає виконаних замовлень.",
            parse_mode="HTML",
            reply_markup=cabinet_menu
        )

        await callback.answer()
        return

    keyboard = []

    for order in completed:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"✅ #{order.id} • {order.service}",
                    callback_data=f"client_order_{order.id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="profile"
            )
        ]
    )

    await callback.message.edit_text(
        "✅ <b>Виконані роботи</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()

@router.callback_query(F.data == "how_to_use")
async def how_to_use(callback: CallbackQuery):

    await callback.message.edit_text(
        "ℹ️ <b>Як користуватись PaitEDU</b>\n\n"

        "📂 <b>Мої замовлення</b>\n"
        "Тут знаходяться всі ваші активні замовлення.\n\n"

        "✅ <b>Виконані роботи</b>\n"
        "Тут зберігаються всі завершені замовлення.\n\n"

        "💬 <b>Зв'язок з менеджером</b>\n"
        "Якщо виникли питання — напишіть менеджеру.\n\n"

        "Бажаємо приємного користування ❤️",

        parse_mode="HTML",
        reply_markup=cabinet_menu
    )

    await callback.answer()


@router.callback_query(F.data.startswith("client_order_"))
async def open_client_order(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    order = get_order_by_id(order_id)

    if not order:
        await callback.answer(
            "Замовлення не знайдено.",
            show_alert=True
        )
        return

    status_names = {
        "new": "🟢 Нова заявка",
        "waiting_payment": "💳 Очікує оплату",
        "paid": "💵 Оплачено",
        "work": "🟡 Виконується",
        "review": "🔍 Перевірка",
        "done": "✅ Завершено",
        "archive": "📦 Архів"
    }

    payment_names = {
        "waiting": "⏳ Очікується",
        "paid": "✅ Оплачено"
    }

    deadline = (
        order.deadline.strftime("%d.%m.%Y")
        if order.deadline
        else "Не встановлено"
    )

    created = order.created_at.strftime("%d.%m.%Y")

    await callback.message.edit_text(
        order_card(
            order=order,
            status_name=status_names.get(order.status, "❓ Невідомо"),
            payment_name=payment_names.get(
                order.payment_status,
                "⏳ Очікується"
            ),
            deadline=deadline,
            created=created,
            progress=build_progress(
                order.status,
                order.payment_status,
                order.price_status
            )
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💬 Написати менеджеру",
                        callback_data="contact_manager"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data="my_orders"
                    )
                ]
            ]
        )
    )

    await callback.answer()

@router.callback_query(F.data == "contact_manager")
async def contact_manager(callback: CallbackQuery, state: FSMContext):

    orders = get_orders_by_user(callback.from_user.id)

    orders = [
        order for order in orders
        if order.status in ["new", "work"]
    ]

    if not orders:

        await state.set_state(OrderState.waiting_general_message)

        await callback.message.edit_text(
            "💬 <b>Зв'язок з менеджером</b>\n\n"
            "Зараз у вас немає активних замовлень.\n\n"
            "Але ви можете поставити будь-яке питання менеджеру.\n\n"
            "✍️ Просто напишіть повідомлення.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="⬅️ На головну",
                            callback_data="back_main"
                        )
                    ]
                ]
            )
        )

        await callback.answer()
        return


    keyboard = []

    for order in orders:

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"🟡 #{order.id} • {order.service}",
                    callback_data=f"client_chat_{order.id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="profile"
            )
        ]
    )

    await callback.message.edit_text(
        "💬 <b>Оберіть замовлення</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()

@router.callback_query(F.data.startswith("client_chat_"))
async def client_chat(callback: CallbackQuery, state: FSMContext):

    order_id = int(callback.data.split("_")[2])

    await state.update_data(order_id=order_id)
    await state.set_state(OrderState.waiting_client_message)

    await callback.message.edit_text(
        f"💬 <b>Чат з менеджером</b>\n\n"
        f"Замовлення <b>№{order_id}</b>\n\n"
        f"Напишіть повідомлення, і воно буде "
        f"відправлене менеджеру.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ На головну",
                        callback_data="back_main"
                    )
                ]
            ]
        )
    )

    await callback.answer()

@router.message(OrderState.waiting_client_message)
async def send_message_to_manager(message: Message, state: FSMContext):

    data = await state.get_data()

    order = get_order_by_id(data["order_id"])

    if not order:
        await message.answer("❌ Замовлення не знайдено.")
        await state.clear()
        return

    status_names = {
        "new": "🟢 Нове",
        "work": "🟡 У роботі",
        "done": "✅ Виконано",
        "archive": "📦 Архів"
    }

    status = status_names.get(order.status, order.status)

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

    sent = await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "╔════════════════════╗\n"
            "  🎓 PaitEDU CRM\n"
            "╚════════════════════╝\n\n"

            f"👤 <b>{order.full_name}</b>\n\n"

            f"📄 Замовлення <b>№{order.id}</b>\n"
            f"📚 {order.service}\n"
            f"📌 <b>{status}</b>\n"
            f"🕒 {current_time}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "💬 <b>Нове повідомлення</b>\n\n"

            f"{message.text}"

            "\n\n━━━━━━━━━━━━━━━━━━"
        ),
        parse_mode="HTML",
        reply_markup=message_card_menu(order.id)
    )

    add_message(
        order_id=order.id,
        sender="client",
        text=message.text,
        telegram_message_id=sent.message_id
    )

    await message.answer(
        "✅ Повідомлення успішно відправлено менеджеру."
    )

    await state.clear()