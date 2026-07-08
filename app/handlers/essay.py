from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.keyboards.essay_menu import essay_menu
from aiogram.fsm.context import FSMContext
from app.states.order_state import OrderState

router = Router()


@router.callback_query(F.data == "service_essay")
async def essay_callback(callback: CallbackQuery, state: FSMContext):

    await state.update_data(service="📄 Реферат")

    await callback.message.edit_text(
        "📄 <b>Реферати</b>\n\n"
        "✅ Виконуємо реферати будь-якої складності.\n\n"
        "📚 Гуманітарні\n"
        "💻 Технічні\n"
        "💼 Економічні\n\n"
        "⏳ Термін виконання:\n"
        "від 1 дня.",
        parse_mode="HTML",
        reply_markup=essay_menu
    )