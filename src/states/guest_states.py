from aiogram.fsm.state import State, StatesGroup


class Guest(StatesGroup):
    guest_main_room = State()