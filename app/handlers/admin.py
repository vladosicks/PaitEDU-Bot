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
from aiogram.fsm.context import FSMContext
from app.states.order_state import OrderState
from app.utils.order_cards import build_admin_order_text
from app.keyboards.price_confirm_menu import price_confirm_menu
from app.database.crud import update_price_status
from aiogram.types import Document
from app.keyboards.payment_ready_menu import payment_ready_menu

from app.utils.constants import *

from app.utils.constants import (
    PRICE_WAITING,
    PRICE_ACCEPTED,
    PRICE_DECLINED
)

from app.database.crud import (
    get_new_orders,
    get_work_orders,
    get_done_orders,
    get_archive_orders,
    get_order_by_id,
    update_order_status,
    get_messages,
    get_orders_count_by_status,
    search_orders,
    update_order_price,
    update_order_document,
    update_pending_price,
    update_payment_status
)

router = Router()

async def open_admin_panel(callback: CallbackQuery):

    new_count = get_orders_count_by_status(STATUS_NEW)
    work_count = get_orders_count_by_status(STATUS_WORK)
    done_count = get_orders_count_by_status(STATUS_DONE)
    archive_count = get_orders_count_by_status(STATUS_ARCHIVE)

    await callback.message.edit_text(
        f"👨‍💼 <b>Адмін-панель</b>\n\n"
        f"📊 <b>Поточний стан CRM</b>\n\n"
        f"🟢 Нові: <b>{new_count}</b>\n"
        f"🟡 В роботі: <b>{work_count}</b>\n"
        f"✅ Виконані: <b>{done_count}</b>\n"
        f"📦 Архів: <b>{archive_count}</b>\n\n"
        f"Оберіть потрібний розділ:",
        parse_mode="HTML",
        reply_markup=admin_menu
    )

    await callback.answer()

    await callback.answer()

@router.callback_query(F.data == "admin_search")
async def admin_search(callback: CallbackQuery, state: FSMContext):

    await state.set_state(OrderState.waiting_search)

    await callback.message.edit_text(
        "🔍 <b>Пошук замовлення</b>\n\n"
        "Введіть:\n"
        "• номер замовлення (15 або #15)\n"
        "• @username\n"
        "• ім'я клієнта",
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(F.text == "/admin")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    new_count = get_orders_count_by_status("new")
    work_count = get_orders_count_by_status("work")
    done_count = get_orders_count_by_status("done")
    archive_count = get_orders_count_by_status("archive")

    await message.answer(
        f"👨‍💼 <b>Адмін-панель</b>\n\n"
        f"📊 <b>Поточний стан CRM</b>\n\n"
        f"🟢 Нові: <b>{new_count}</b>\n"
        f"🟡 В роботі: <b>{work_count}</b>\n"
        f"✅ Виконані: <b>{done_count}</b>\n"
        f"📦 Архів: <b>{archive_count}</b>\n\n"
        f"Оберіть потрібний розділ:",
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

    text = build_admin_order_text(
        order,
        history
    )
    try:
        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=order_card_menu(order.id, order.status, order.price_status)
        )
    except Exception:
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=order_card_menu(order.id, order.status, order.price_status)
        )

    await callback.answer()

@router.callback_query(F.data.startswith("open_order_"))
async def open_order_from_notification(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    callback.data = f"order_{order_id}"

    await open_order(callback)


@router.callback_query(F.data.startswith("set_price_"))
async def set_price(callback: CallbackQuery, state: FSMContext):

    order_id = int(callback.data.split("_")[2])

    await state.update_data(order_id=order_id)
    await state.set_state(OrderState.waiting_price)

    await callback.message.answer(
        f"💰 <b>Встановлення ціни</b>\n\n"
        f"Замовлення №<b>{order_id}</b>\n\n"
        "Введіть тільки число.\n"
        "Наприклад: <b>800</b>",
        parse_mode="HTML"
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
            f"🎉 <b>Ваше замовлення №{order.id} виконано!</b>\n\n"
            f"📚 Послуга: <b>{order.service}</b>\n\n"
            "✅ Робота вже готова.\n\n"
            "💳 Для отримання готової роботи натисніть кнопку нижче та зв'яжіться з менеджером.\n\n"
            "Після підтвердження оплати документ буде автоматично надіслано в цей чат."
        ),
        parse_mode="HTML",
        reply_markup=payment_ready_menu(order.id)
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

@router.callback_query(F.data.startswith("order_archive_"))
async def order_archive(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    update_order_status(order_id, "archive")

    await callback.answer("📦 Замовлення перенесено в архів")

    orders = get_archive_orders()

    if not orders:
        await callback.message.edit_text(
            "📦 Архів поки порожній."
        )
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
        "📦 <b>Архів замовлень</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

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

@router.callback_query(F.data == "orders_archive")
async def show_archive_orders(callback: CallbackQuery):

    orders = get_archive_orders()

    if not orders:
        await callback.message.edit_text(
            "📦 Архів поки порожній."
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
        "📦 <b>Архів замовлень</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await callback.answer()

@router.message(OrderState.waiting_search)
async def process_search(message: Message, state: FSMContext):

    orders = search_orders(message.text)

    if not orders:
        await message.answer(
            "❌ Замовлення не знайдено."
        )
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
                callback_data="admin_back"
            )
        ]
    )

    await message.answer(
        "🔍 <b>Результати пошуку</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=keyboard
        )
    )

    await state.clear()


@router.message(OrderState.waiting_price)
async def process_price(message: Message, state: FSMContext):

    if not message.text.isdigit():

        await message.answer(
            "❌ Введіть тільки число.\n\n"
            "Наприклад: 800"
        )

        return

    data = await state.get_data()

    order_id = data["order_id"]

    price = int(message.text)

    update_pending_price(order_id, price)

    order = get_order_by_id(order_id)

    print(">>> Відправляємо клієнту")
    print(order.user_id)
    print(price)

    await message.bot.send_message(
        chat_id=order.user_id,
        text=(
            f"💰 <b>Ваше замовлення оцінено</b>\n\n"
            f"📄 Замовлення №<b>{order.id}</b>\n"
            f"📚 Послуга: <b>{order.service}</b>\n\n"
            f"💵 Вартість: <b>{price} грн</b>\n\n"
            "Будь ласка, підтвердіть, чи вас влаштовує ця вартість."
        ),
        parse_mode="HTML",
        reply_markup=price_confirm_menu(order.id)
    )

    print(">>> Повідомлення відправлено")

    await message.answer(
        f"✅ Ціну встановлено.\n\n"
        f"💰 {price} грн",
        parse_mode="HTML"
    )

    await state.clear()

@router.callback_query(F.data.startswith("start_work_"))
async def start_work(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    update_order_status(
        order_id,
        STATUS_WORK
    )

    order = get_order_by_id(order_id)

    await callback.bot.send_message(
        chat_id=order.user_id,
        text=(
            "🟡 <b>Ми розпочали виконання вашого замовлення.</b>\n\n"
            f"📄 Замовлення №<b>{order.id}</b>\n\n"
            "Наш спеціаліст уже працює над вашим замовленням.\n"
            "Ми повідомимо вас, коли воно буде готове."
        ),
        parse_mode="HTML"
    )

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

    text = build_admin_order_text(
        order,
        history
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=order_card_menu(
            order.id,
            order.status,
            order.price_status
        )
    )

    await callback.answer(
        "✅ Роботу розпочато."
    )

@router.callback_query(F.data.startswith("upload_file_"))
async def upload_file(callback: CallbackQuery, state: FSMContext):

    order_id = int(callback.data.split("_")[2])

    await state.update_data(order_id=order_id)

    await state.set_state(OrderState.waiting_document)

    await callback.message.answer(
        "📎 <b>Надішліть готовий документ.</b>\n\n"
        "Підтримуються:\n"
        "• PDF\n"
        "• DOCX\n"
        "• ZIP\n"
        "• RAR\n"
        "• будь-які інші документи Telegram",
        parse_mode="HTML"
    )

    await callback.answer()

@router.message(OrderState.waiting_document, F.document)
async def receive_document(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    order_id = data["order_id"]

    file = message.document

    update_order_document(
        order_id=order_id,
        file_id=file.file_id,
        file_name=file.file_name
    )

    await message.answer(
        "✅ <b>Файл успішно завантажено.</b>\n\n"
        f"📄 {file.file_name}",
        parse_mode="HTML"
    )

    await state.clear()

@router.callback_query(F.data.startswith("confirm_payment_"))
async def confirm_payment(callback: CallbackQuery):

    order_id = int(callback.data.split("_")[2])

    order = get_order_by_id(order_id)

    if not order.document_file_id:

        await callback.answer(
            "❌ Спочатку завантажте готовий документ.",
            show_alert=True
        )

        return

    update_payment_status(
        order.id,
        PAYMENT_PAID
    )

    await callback.bot.send_message(
        chat_id=order.user_id,
        text=(
            "🎉 <b>Оплату підтверджено!</b>\n\n"
            "Дякуємо за оплату.\n"
            "Вашу готову роботу надіслано нижче 👇"
        ),
        parse_mode="HTML"
    )

    await callback.bot.send_document(
        chat_id=order.user_id,
        document=order.document_file_id,
        caption=f"📄 {order.document_name}"
    )

    await callback.message.answer(
        "✅ Роботу успішно видано клієнту."
    )

    await callback.answer()

@router.message(OrderState.waiting_document)
async def waiting_document_error(message: Message):

    await message.answer(
        "❌ Будь ласка, надішліть документ.\n\n"
        "PDF, DOCX, ZIP або інший файл."
    )
