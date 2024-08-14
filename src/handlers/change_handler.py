from aiogram import Router, F
from typing import Optional, List, Union, Iterator, Any, Dict, cast
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, MessageEntity, UNSET_PARSE_MODE, InputMedia, \
    InputMediaPhoto, InputMediaAudio, InputMediaVideo, InputMediaDocument
from config import bot
from src.keyboards.user_keyboard import (
    back_keyboard,
    genre_of_work_keyboard,
    profile_edit_keyboard,
    profile_keyboard,
    registered_keyboard,
    registration_edit_keyboard,
    skip_keyboard,
    user_keyboard_button,
    user_keyboard,
    guild_keyboard_button,
    guild_keyboard,
    genres_of_work,
    profile_keyboard_buttons,
    edit_profile_buttons,
    back_button
)
from src.phrases import (
    BACK_TO_MENU,
    BACK_TO_PROFILE,
    CHANGE_FIO_SUCCESS,
    COMPANY_NAME,
    EDIT_PROFILE,
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

@change_router.message(F.text == profile_keyboard_buttons["button1"], User.profile)
async def edit_profile(message: Message, state: FSMContext):
    await message.answer(EDIT_PROFILE, reply_markup=profile_edit_keyboard())
    await state.set_state(Change.profile_change)


@change_router.message(F.text == edit_profile_buttons["button1"], Change.profile_change)
async def edit_profile_fio(message: Message, state: FSMContext):
    await message.answer(SURVEY_FIO_EXAMPLE, reply_markup=back_keyboard())
    await state.set_state(Change.fio)

@change_router.message(StateFilter(Change.fio,Change.waiting_for_fio), F.text == back_button['button1'])
async def edit_profile_back(message: Message, state: FSMContext):
    await message.answer(BACK_TO_PROFILE, reply_markup=profile_edit_keyboard()) #Здесь добавлять стейты для возврата назад
    await state.set_state(Change.profile_change)

@change_router.message(Change.fio)
async def edit_profile_waiting_fio(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        fio = message.text
        if validate_fio(fio):
            supabase.table("UserData").update({"fio": fio}).eq("chat_id", chat_id).execute()
            await state.set_state(Change.profile_change)
            await message.answer(CHANGE_FIO_SUCCESS + " на " + fio , reply_markup=profile_edit_keyboard())
        else:
            await message.answer(SURVEY_FIO_VALIDATION, reply_markup=back_keyboard())
    except Exception as e:
        print("Error in handler edit_profile_waiting_fio", e)


@change_router.message(F.text == edit_profile_buttons["button8"], Change.profile_change)
async def edit_profile_back_to_main_menu(message: Message, state: FSMContext):
    await message.answer(BACK_TO_MENU, reply_markup=registered_keyboard())
    await state.set_state(User.registration_end)

