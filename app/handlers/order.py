from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Document
from aiogram.fsm.context import FSMContext

from app.states.order_state import OrderState

from app.keyboards.order_menu import order_menu
from app.keyboards.main_menu import main_menu
from app.ui.cards import success_card

from app.database.crud import add_order

from app.config.settings import ADMIN_ID
from app.keyboards.new_order_notification import new_order_notification

router = Router()

@router.callback_query(F.data.endswith("_order"))
async def start_order(callback: CallbackQuery, state: FSMContext):

    services = {
        "essay_order": "📄 Реферат",
        "coursework_order": "📚 Курсова робота",
        "diploma_order": "🎓 Дипломна робота",
        "presentation_order": "📊 Презентація",
        "translation_order": "🌍 Переклад",
        "other_order": "📦 Інше"
    }

    service = services.get(callback.data)

    await state.update_data(service=service)
    await state.set_state(OrderState.waiting_for_order)

    await callback.message.edit_text(
        "📝 <b>Опишіть ваше замовлення.</b>\n\n"
        "Також можна одразу прикріпити файл.", 
        parse_mode="HTML",
        reply_markup=order_menu
    )

    await callback.answer()

@router.callback_query(F.data == "order_cancel")
async def cancel_order(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.edit_text(
        "📚 Оберіть потрібну послугу:",
        reply_markup=main_menu
    )

    await callback.answer()

@router.message(OrderState.waiting_for_order, F.text)
async def receive_order(message: Message, state: FSMContext):

    data = await state.get_data()

    service = data.get("service", "Невідома послуга")

    order = add_order(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name,
        service=service,
        description=message.text
    )

    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🆕 <b>Нове замовлення #{order.id}</b>\n\n"
            f"👤 <b>Клієнт:</b> {order.full_name}\n"
            f"🆔 <b>ID:</b> <code>{order.user_id}</code>\n"
            f"📨 <b>Username:</b> @{order.username or 'немає'}\n\n"
            f"📚 <b>Послуга:</b> {order.service}\n\n"
            f"📝 <b>Опис:</b>\n"
            f"{order.description}"
        ),
        parse_mode="HTML",
        reply_markup=new_order_notification(order.id)
    )

    await message.answer(
        success_card(
            "Замовлення отримано",
            (
                "Ми вже отримали вашу заявку.\n\n"
                "👨‍💼 Менеджер перевірить її найближчим часом "
                "та зв'яжеться з вами."
            )
        ),
        parse_mode="HTML"
    )

    await state.clear()

@router.message(OrderState.waiting_for_order, F.document)
async def receive_document(message: Message, state: FSMContext):

    data = await state.get_data()

    service = data.get("service", "Невідома послуга")

    order = add_order(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name,
        service=service,
        description=message.caption or "Файл без опису"
    )

    await message.bot.send_document(
        chat_id=ADMIN_ID,
        document=message.document.file_id,
        caption=(
            f"🆕 <b>Нове замовлення #{order.id}</b>\n\n"
            f"👤 <b>Клієнт:</b> {order.full_name}\n"
            f"🆔 <b>ID:</b> <code>{order.user_id}</code>\n"
            f"📨 <b>Username:</b> @{order.username or 'немає'}\n\n"
            f"📚 <b>Послуга:</b> {order.service}\n\n"
            f"📝 <b>Опис:</b>\n"
            f"{message.caption or 'Без опису'}"
        ),
        parse_mode="HTML",
        reply_markup=new_order_notification(order.id)
    )

    await message.answer(
        "✅ Файл отримано!\n\n"
        "Найближчим часом ми зв'яжемося з вами."
    )

    await state.clear()

@router.message(OrderState.waiting_for_order, F.photo)
async def receive_photo(message: Message, state: FSMContext):

    data = await state.get_data()

    service = data.get("service", "Невідома послуга")

    order = add_order(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name,
        service=service,
        description=message.caption or "Фото без опису"
    )

    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=(
            f"🆕 <b>Нове замовлення #{order.id}</b>\n\n"
            f"👤 <b>Клієнт:</b> {order.full_name}\n"
            f"🆔 <b>ID:</b> <code>{order.user_id}</code>\n"
            f"📨 <b>Username:</b> @{order.username or 'немає'}\n\n"
            f"📚 <b>Послуга:</b> {order.service}\n\n"
            f"📝 <b>Опис:</b>\n"
            f"{message.caption or 'Без опису'}"
        ),
        parse_mode="HTML",
        reply_markup=new_order_notification(order.id)
    )

    await message.answer(
        "✅ Фото отримано!\n\n"
        "Найближчим часом ми зв'яжемося з вами."
    )

    await state.clear()