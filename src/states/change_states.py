from aiogram.fsm.state import State, StatesGroup


class Change(StatesGroup):
    profile_change = State()
    fio = State()
    waiting_for_fio = State()
    survey_media = State()
    phone = State()
    waiting_for_phone = State()
    mail = State()
    waiting_for_mail = State()
    guild = State()
    company = State()
    waiting_for_company = State()
    category = State()
