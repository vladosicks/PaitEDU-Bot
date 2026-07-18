from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    waiting_for_order = State()
    waiting_admin_reply = State()
    waiting_client_reply = State()
    waiting_search = State()
    waiting_client_message = State()
    waiting_general_message = State()

    waiting_price = State()
    waiting_price_decline = State()
    waiting_document = State()
    waiting_manager_comment = State()