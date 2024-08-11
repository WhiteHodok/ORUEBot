from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    greetings = State()
    main = State()