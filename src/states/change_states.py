from aiogram.fsm.state import State, StatesGroup


class Change(StatesGroup):
    profile_change = State()
    fio = State()
    waiting_for_fio = State()
    survey_media = State()
    phone = State()
    mail = State()
    guild = State()
    company = State()
    category = State()
