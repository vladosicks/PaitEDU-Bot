from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from app.config.settings import ADMIN_ID
from app.keyboards.admin_menu import admin_menu
from app.keyboards.admin_orders_menu import admin_orders_menu
from app.keyboards.order_card_menu import order_card_menu


from app.database.crud import (
    get_new_orders,
    get_work_orders,
    get_done_orders,
    get_order_by_id,
    update_order_status,
    get_messages,
)

router = Router()

async def open_admin_panel(callback: CallbackQuery):

    await callback.message.edit_text(
        "👨‍💼 <b>Адмін-панель</b>\n\n"
        "Ласкаво просимо!",
        parse_mode="HTML",
        reply_markup=admin_menu
    )

    await callback.answer()


@router.message(F.text == "/admin")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👨‍💼 <b>Адмін-панель</b>\n\n"
        "Ласкаво просимо!",
        parse_mode="HTML",
        reply_markup=admin_menu
    )

@router.callback_query(F.data == "admin_orders")
async def admin_orders(callback: CallbackQuery):

    await callback.message.edit_text(
        "📋 <b>Замовлення</b>\n\n"
        "Оберіть категорію:",
        parse_mode="HTML",
        reply_markup=admin_orders_menu
    )

    await callback.answer()


@router.callback_query(F.data == "orders_new")
async def show_new_orders(callback: CallbackQuery):

    orders = get_new_orders()

    if not orders:
        await callback.message.edit_text(
            "📭 Нових замовлень поки немає."
        )
        await callback.answer()
        return

    keyboard = []

    for order in orders:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"#{order.id} • {order.full_name} • {order.service}",
                    callback_data=f"open_order_{order.id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_orders"
            )
        ]
    )

    await callback.message.edit_text(
        "🟢 <b>Нові замовлення</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()


@router.callback_query(F.data.startswith("open_order_"))
async def open_order(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    order = get_order_by_id(order_id)

    messages = get_messages(order.id)

    history = ""

    for msg in messages:

        if msg.sender == "admin":
            sender = "👨‍💼 Менеджер"
        else:
            sender = "👤 Клієнт"

        history += f"{sender}:\n{msg.text}\n\n"

    if not history:
        history = "Історія повідомлень поки порожня."


    if not order:
        await callback.answer(
            "Замовлення не знайдено.",
            show_alert=True
        )
        return

    text = (
        f"📄 <b>Замовлення #{order.id}</b>\n\n"
        f"👤 <b>Клієнт:</b> {order.full_name}\n"
        f"🆔 <b>ID:</b> <code>{order.user_id}</code>\n"
        f"📨 <b>Username:</b> @{order.username or 'немає'}\n\n"
        f"📚 <b>Послуга:</b> {order.service}\n\n"
        f"📝 <b>Опис:</b>\n"
        f"{order.description or '—'}\n\n"
        f"📅 <b>Дата:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"📌 <b>Статус:</b> {order.status}"
        f"\n\n"
        f"──────────────\n"
        f"<b>💬 Історія листування</b>\n\n"
        f"{history}"
    )

    try:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=order_card_menu(order.id, order.status)
        )
    except Exception:
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=order_card_menu(order.id, order.status)
        )

    await callback.answer()


@router.callback_query(F.data.startswith("order_work_"))
async def order_work(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    update_order_status(order_id, "work")

    order = get_order_by_id(order_id)

    await callback.bot.send_message(
        chat_id=order.user_id,
        text=(
            f"🟡 Ваше замовлення №{order.id} взято в роботу.\n\n"
            f"📚 Послуга: {order.service}\n\n"
            "Наш спеціаліст уже працює над вашим замовленням.\n"
            "Якщо виникнуть уточнення — ми обов'язково зв'яжемося з вами."
        )
    )

    await callback.answer("🟡 Замовлення взято в роботу")

    await open_order(callback)

@router.callback_query(F.data.startswith("order_done_"))
async def order_done(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    update_order_status(order_id, "done")

    order = get_order_by_id(order_id)

    await callback.bot.send_message(
        chat_id=order.user_id,
        text=(
            f"🎉 Ваше замовлення №{order.id} виконано!\n\n"
            f"📚 Послуга: {order.service}\n\n"
            "Дякуємо, що обрали нас ❤️\n"
            "Якщо виникнуть нові завдання — будемо раді допомогти."
        )
    )

    await callback.answer("✅ Замовлення виконано")

    await open_order(callback)


@router.callback_query(F.data == "orders_work")
async def show_work_orders(callback: CallbackQuery):

    orders = get_work_orders()

    if not orders:
        await callback.message.edit_text(
            "📭 Замовлень у роботі поки немає."
        )
        await callback.answer()
        return

    keyboard = []

    for order in orders:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"#{order.id} • {order.full_name} • {order.service}",
                    callback_data=f"open_order_{order.id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_orders"
            )
        ]
    )

    await callback.message.edit_text(
        "🟡 <b>Замовлення в роботі</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()

@router.callback_query(F.data == "orders_done")
async def show_done_orders(callback: CallbackQuery):

    orders = get_done_orders()

    if not orders:
        await callback.message.edit_text(
            "📭 Виконаних замовлень поки немає."
        )
        await callback.answer()
        return

    keyboard = []

    for order in orders:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"#{order.id} • {order.full_name} • {order.service}",
                    callback_data=f"open_order_{order.id}"
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin_orders"
            )
        ]
    )

    await callback.message.edit_text(
        "✅ <b>Виконані замовлення</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()

@router.callback_query(F.data.startswith("order_return_"))
async def order_return(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    update_order_status(order_id, "work")

    order = get_order_by_id(order_id)

    await callback.bot.send_message(
        chat_id=order.user_id,
        text=(
            f"🟡 Ваше замовлення №{order.id} знову перебуває в роботі.\n\n"
            "Потрібне невелике доопрацювання або уточнення.\n"
            "Ми вже працюємо над цим і повідомимо вас після завершення."
        )
    )

    await callback.answer("🟡 Замовлення повернуто в роботу")

    await open_order(callback)

@router.callback_query(F.data == "admin_back")
async def admin_back(callback: CallbackQuery):

    await callback.message.edit_text(
        "👨‍💼 <b>Адмін-панель</b>\n\n"
        "Ласкаво просимо!",
        parse_mode="HTML",
        reply_markup=admin_menu
    )

    await callback.answer()
