from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    greetings = State()
    main = State()
    registration = State()
    registration_start = State()
    registration_handle_fio_start = State()
    registration_handle_fio_end = State()
    registration_handle_guild_start = State()
    registration_handle_guild_end = State()
    registration_handle_company_name_start = State()
    registration_handle_company_name_end = State()
    registration_handle_genre_of_work = State()
    registration_handle_photo_survey_start = State()
    registration_handle_photo_survey_end = State()
    registration_handle_phone_number_start = State()
    registration_handle_phone_number_end = State()
    registration_handle_email_start = State()
    registration_end = State()
    profile = State()

