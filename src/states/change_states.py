from aiogram.fsm.state import State, StatesGroup


class Change(StatesGroup):
    fio = State()
    survey_media = State()
    phone = State()
    mail = State()
    guild = State()
    company = State()
    category = State()
