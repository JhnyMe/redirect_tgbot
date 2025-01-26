from aiogram.fsm.state import State,StatesGroup

class UserStates(StatesGroup):
    waiting_for_add = State()
    waiting_for_delete = State()
    waiting_for_send_video = State()
    waiting_for_confirmation = State()