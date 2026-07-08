from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.states.order_state import OrderState

router = Router()


@router.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: CallbackQuery):

    user_id = int(callback.data.split("_")[1])

    await callback.bot.send_message(
        chat_id=user_id,
        text=(
            "✅ Ваше замовлення прийнято в роботу!\n\n"
            "Наш менеджер вже займається вашим замовленням."
        )
    )

    #await callback.message.edit_reply_markup(reply_markup=None)

    await callback.answer("Замовлення прийнято ✅")

@router.callback_query(F.data.startswith("reply_"))
async def reply_to_user(callback: CallbackQuery, state: FSMContext):

    user_id = int(callback.data.split("_")[1])

    await state.update_data(reply_user_id=user_id)
    await state.set_state(OrderState.waiting_admin_reply)

    await callback.message.answer(
        "💬 Напишіть повідомлення для клієнта."
    )

    await callback.answer()

@router.callback_query(F.data.startswith("done_"))
async def done_order(callback: CallbackQuery):

    user_id = int(callback.data.split("_")[1])

    await callback.bot.send_message(
        chat_id=user_id,
        text=(
            "🎉 Ваше замовлення виконано!\n\n"
            "Будемо дуже вдячні, якщо ви залишите короткий відгук ❤️"
        )
    )

    await callback.answer("Клієнту відправлено запит на відгук ⭐")

@router.message(OrderState.waiting_admin_reply)
async def send_reply(message: Message, state: FSMContext):

    data = await state.get_data()
    user_id = data["reply_user_id"]

    await message.bot.send_message(
        chat_id=user_id,
        text=(
            "💬 Повідомлення від менеджера:\n\n"
            f"{message.text}"
        )
    )

    await state.clear()

    await message.answer(
        "✅ Повідомлення успішно відправлено клієнту."
    )