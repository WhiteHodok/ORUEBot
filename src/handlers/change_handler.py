from aiogram import Router, F
from typing import Optional, List, Union, Iterator, Any, Dict, cast
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, MessageEntity, UNSET_PARSE_MODE, InputMedia, \
    InputMediaPhoto, InputMediaAudio, InputMediaVideo, InputMediaDocument
from config import bot
from src.keyboards.user_keyboard import (
    genre_of_work_keyboard,
    registration_edit_keyboard,
    skip_keyboard,
    user_keyboard_button,
    user_keyboard,
    guild_keyboard_button,
    guild_keyboard,
    genres_of_work
)
from src.phrases import (
    COMPANY_NAME,
    EMAIL_ADDRESS,
    EMAIL_SKIP,
    EMAIL_SUCCESS,
    EMAIL_VALIDATION,
    GENRE_OF_WORK,
    PHONE_NUMBER_VALIDATION,
    PHONE_SUCCESS,
    REGISTRATION_END_ASK,
    SURVEY_EXAMPLE,
    SURVEY_EXAMPLE_ERROR,
    SURVEY_START_REGISTRATION,
    SURVEY_FIO_EXAMPLE,
    SURVEY_FIO_VALIDATION,
    SURVEY_GUILD_EXAMPLE,
    SKIP_BUTTON,
    CATEGORIES, MEDIA_CAPTION, MEDIA_SUCCESS, SURVEY_PHONE_NUMBER, MEDIA_VALIDATION
)
from src.states.user_states import User
from src.states.change_states import Change
from src.middlewares.user_verification_middleware import VerificationMiddleware
from src.middlewares.album_middleware import *
from src.handlers.user_validation import (
    validate_fio,
    validate_phone_number,
    validate_email
)
from src.handlers.user_handler import user_router
from src.handlers.user_handler import to_input_media
from config import supabase

change_router = Router()

change_router.message.middleware(VerificationMiddleware())
change_router.message.middleware(AlbumMiddleware())



