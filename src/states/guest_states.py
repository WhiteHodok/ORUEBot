from aiogram.fsm.state import State, StatesGroup


class Guest(StatesGroup):
    main = State()