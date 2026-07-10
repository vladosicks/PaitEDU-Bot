from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    waiting_for_order = State()
    waiting_admin_reply = State()
    waiting_client_reply = State()