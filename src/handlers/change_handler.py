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
    hash_buttons,
    profile_edit_keyboard,
    profile_keyboard,
    registered_keyboard,
    reset_genres_of_work,
    skip_keyboard,
    user_keyboard_button,
    user_keyboard,
    guild_keyboard_button,
    guild_keyboard,
    genres_of_work,
    profile_keyboard_buttons,
    edit_profile_buttons,
    back_button,
    guild_edit_profile,
    guild_edit_keyboard

)
from src.phrases import (
    BACK_TO_MENU,
    BACK_TO_PROFILE,
    CHANGE_CATRGORY,
    CHANGE_CATRGORY_SUCCESS,
    CHANGE_FIO_SUCCESS,
    CHANGE_MEDIA,
    COMPANY_NAME,
    EDIT_PROFILE,
    EMAIL_ADDRESS,
    EMAIL_SKIP,
    EMAIL_SUCCESS,
    EMAIL_VALIDATION,
    GENRE_OF_WORK,
    GENRE_OF_WORK_VALIDATION,
    MEDIA_VALIDATION,
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
    CATEGORIES,
    MEDIA_CAPTION,
    MEDIA_SUCCESS,
    SURVEY_PHONE_NUMBER,
    CHANGE_PHONE_SUCCESS,
    CHANGE_EMAIL_SUCCESS,
    CHANGE_COMPANY_SUCCESS,
    CHANGE_GUILD_SUCCESS
)
from src.repo.SurveyRepo import SurveyRepository
from src.repo.UserDataRepo import UserDataRepository
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
from config import supabase
from src.repo import UserDataRepo
from src.repo import SurveyRepo

user_repo = UserDataRepository(supabase)
survey_repo = SurveyRepository(supabase)

change_router = Router()

change_router.message.middleware(VerificationMiddleware())
change_router.message.middleware(AlbumMiddleware())




@change_router.message(F.text == edit_profile_buttons["button1"], Change.profile_change)
async def edit_profile_fio(message: Message, state: FSMContext):
    await message.answer(SURVEY_FIO_EXAMPLE, reply_markup=back_keyboard())
    await state.set_state(Change.fio)


@change_router.message(
    StateFilter(Change.fio, Change.waiting_for_fio, Change.phone, Change.waiting_for_phone, Change.mail,
                Change.waiting_for_mail, Change.company, Change.guild, Change.category, Change.survey_media),
    F.text == back_button['button1'])
async def edit_profile_back(message: Message, state: FSMContext):
    await message.answer(BACK_TO_PROFILE,
                         reply_markup=profile_edit_keyboard())  # Здесь добавлять стейты для возврата назад
    await state.set_state(Change.profile_change)


@change_router.message(Change.fio)
async def edit_profile_waiting_fio(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        fio = message.text
        if validate_fio(fio):
            user_repo.update_field(chat_id, "fio", fio)
            await state.set_state(Change.profile_change)
            await message.answer(CHANGE_FIO_SUCCESS + " на " + fio, reply_markup=profile_edit_keyboard())
        else:
            await message.answer(SURVEY_FIO_VALIDATION, reply_markup=back_keyboard())
    except Exception as e:
        print("Error in handler edit_profile_waiting_fio", e)


@change_router.message(F.text == edit_profile_buttons["button5"], Change.profile_change)
async def edit_profile_phone(message: Message, state: FSMContext):
    await message.answer(SURVEY_PHONE_NUMBER, reply_markup=back_keyboard())
    await state.set_state(Change.phone)


@change_router.message(Change.phone)
async def edit_profile_waiting_phone(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        phone = message.text
        if validate_phone_number(phone):
            user_repo.update_field(chat_id, "phone", phone)
            await state.set_state(Change.profile_change)
            await message.answer(CHANGE_PHONE_SUCCESS + " на " + phone, reply_markup=profile_edit_keyboard())
        else:
            await message.answer(PHONE_NUMBER_VALIDATION, reply_markup=back_keyboard())
    except Exception as e:
        print("Error in handler edit_profile_waiting_phone", e)


@change_router.message(F.text == edit_profile_buttons["button6"], Change.profile_change)
async def edit_profile_email(message: Message, state: FSMContext):
    await message.answer(EMAIL_ADDRESS, reply_markup=back_keyboard())
    await state.set_state(Change.mail)


@change_router.message(Change.mail)
async def edit_profile_waiting_email(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        email = message.text
        if validate_email(email):
            user_repo.update_field(chat_id, "email", email)
            await state.set_state(Change.profile_change)
            await message.answer(CHANGE_EMAIL_SUCCESS + " на " + email, reply_markup=profile_edit_keyboard())
        else:
            await message.answer(EMAIL_VALIDATION, reply_markup=back_keyboard())
    except Exception as e:
        print("Error in handler edit_profile_waiting_email", e)


@change_router.message(F.text == edit_profile_buttons["button3"], Change.profile_change)
async def edit_profile_change_company_name(message: Message, state: FSMContext):
    await message.answer(COMPANY_NAME, reply_markup=back_keyboard())
    await state.set_state(Change.company)


@change_router.message(Change.company)
async def edit_profile_change_company_name(message: Message, state: FSMContext):
    chat_id = message.chat.id
    company_name = message.text
    user_repo.update_field(chat_id, "company", company_name)
    await state.set_state(Change.profile_change)
    await message.answer(CHANGE_COMPANY_SUCCESS + " на " + company_name, reply_markup=profile_edit_keyboard())


@change_router.message(F.text == edit_profile_buttons["button2"], Change.profile_change)
async def edit_profile_change_guild(message: Message, state: FSMContext):
    await message.answer(SURVEY_GUILD_EXAMPLE, reply_markup=guild_edit_keyboard())
    await state.set_state(Change.guild)


@change_router.message(F.text == guild_edit_profile["guild1"], Change.guild)
async def edit_profile_change_guild_parser_number1(message: Message, state: FSMContext):
    chat_id = message.chat.id
    guild = message.text
    user_repo.update_field(chat_id, "guild", guild)
    await state.set_state(Change.profile_change)
    await message.answer(CHANGE_GUILD_SUCCESS + " на " + guild, reply_markup=profile_edit_keyboard())


@change_router.message(F.text == guild_edit_profile["guild2"], Change.guild)
async def edit_profile_change_guild_parser_number2(message: Message, state: FSMContext):
    chat_id = message.chat.id
    guild = message.text
    user_repo.update_field(chat_id, "guild", guild)
    await state.set_state(Change.profile_change)
    await message.answer(CHANGE_GUILD_SUCCESS + " на " + guild, reply_markup=profile_edit_keyboard())


@change_router.message(F.text == guild_edit_profile["guild3"], Change.guild)
async def edit_profile_change_guild_parser_number3(message: Message, state: FSMContext):
    chat_id = message.chat.id
    guild = message.text
    user_repo.update_field(chat_id, "guild", guild)
    await state.set_state(Change.profile_change)
    await message.answer(CHANGE_GUILD_SUCCESS + " на " + guild, reply_markup=profile_edit_keyboard())

@change_router.message(F.text == edit_profile_buttons["button4"], Change.profile_change) 
async def edit_profile_change_category(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        await bot.send_message(chat_id, CHANGE_CATRGORY, reply_markup=back_keyboard())
        await message.answer(GENRE_OF_WORK, reply_markup=genre_of_work_keyboard())
        await state.set_state(Change.category)
    except Exception as e:
        print("Error in edit_profile_change_category:", e)

hash_to_genre = {hash_buttons(genre): genre for genre in genres_of_work.keys()}
       
@change_router.callback_query(Change.category)
async def edit_profile_change_category_final(callback_query: CallbackQuery, state: FSMContext):
    try:
        chat_id = callback_query.message.chat.id
        genre_hash = callback_query.data
        
        if genre_hash == "confirm":
            # Подтверждение выбора: получаем оригинальные жанры по их состоянию
            selected_genres = [genre for genre, selected in genres_of_work.items() if selected]
            if selected_genres:
                # Сохраняем оригинальные названия жанров в состояние
                await state.update_data(genres_of_work=selected_genres)
                await callback_query.message.answer("Вы выбрали следующие категории:\n" + "\n".join(selected_genres))
                await bot.send_message(chat_id, CHANGE_CATRGORY_SUCCESS, reply_markup=profile_edit_keyboard())
                user_repo.update_field(chat_id, "genre_work", selected_genres)
                reset_genres_of_work()
                await state.set_state(Change.profile_change)
            else:
                await callback_query.answer("Выберите хотя бы одну категорию!", show_alert=True)
        else:
            # Находим оригинальный жанр по хешу
            genre = hash_to_genre.get(genre_hash, None)
            if genre:
                # Переключаем выбранность жанра
                genres_of_work[genre] = not genres_of_work[genre]
                await callback_query.message.edit_reply_markup(reply_markup=genre_of_work_keyboard())
            else:
                await callback_query.answer("Выберите категории", show_alert=True)
    except Exception as e:
        print("Error in handle_genre_of_work_start:", e)


@change_router.message(F.text == edit_profile_buttons["button7"], Change.profile_change)
async def edit_profile_change_media(message: Message, state: FSMContext):
    try: 
        chat_id = message.chat.id
        await bot.send_message(chat_id, CHANGE_MEDIA, reply_markup=back_keyboard())
        await state.set_state(Change.survey_media)
    except Exception as e:
        print("Error in edit_profile_change_media:", e)

@change_router.message(Change.survey_media)
async def edit_profile_change_media_final(message: Message, state: FSMContext, album:list = None):
    chat_id = message.chat.id
    if album is None:
        content_type = message.content_type
        try:
            match content_type:
                case 'text':
                    if survey_repo.get_user_order_data(chat_id):
                        survey_repo.delete_user_data(chat_id)
                    survey_repo.insert_field(chat_id, "text", message.text)
                    await bot.send_message(chat_id, MEDIA_SUCCESS,reply_markup=profile_edit_keyboard())
                    await state.set_state(Change.profile_change)
                case 'photo':
                    if survey_repo.get_user_order_data(chat_id):
                        survey_repo.delete_user_data(chat_id)
                    fields_to_insert = {
                        "chat_id": chat_id,
                        "photo_id": message.photo[-1].file_id,  # Сохраняем ID изображения
                        "text": message.caption  # Сохраняем caption как текст
                    }
                    survey_repo.insert_fields(chat_id, fields_to_insert)
                    await bot.send_message(chat_id, MEDIA_SUCCESS, reply_markup=profile_edit_keyboard())
                    await state.set_state(Change.profile_change)
                case 'video':
                    if survey_repo.get_user_order_data(chat_id):
                        survey_repo.delete_user_data(chat_id)
                    field_to_insert = {
                        "chat_id": chat_id,
                        "video_id": message.video.file_id,  # Сохраняем ID видео
                        "text": message.caption  # Сохраняем caption как текст
                    }
                    survey_repo.insert_fields(chat_id, field_to_insert)
                    await bot.send_message(chat_id, MEDIA_SUCCESS, reply_markup=profile_edit_keyboard())
                    await state.set_state(Change.profile_change)
                case 'document':
                    if survey_repo.get_user_order_data(chat_id):
                        survey_repo.delete_user_data(chat_id)
                    field_to_insert = {
                        "chat_id": chat_id,
                        "document_id": message.document.file_id,  # Сохраняем ID документа
                        "text": message.caption  # Сохраняем caption как текст
                    }
                    survey_repo.insert_fields(chat_id, field_to_insert)
                    await bot.send_message(chat_id, MEDIA_SUCCESS, reply_markup=profile_edit_keyboard())
                    await state.set_state(Change.profile_change)
                case _:
                    await state.set_state(Change.survey_media)
                    await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=back_keyboard())
        except Exception as e:
            print("Error in handle_media:", e)
            await state.set_state(Change.survey_media)
            await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=back_keyboard())
    else:
        try:
            if survey_repo.get_user_order_data(chat_id):
                survey_repo.delete_user_data(chat_id)
            media_ids = [content.photo[-1].file_id if content.photo else content.video.file_id for content in album]
            caption = album[0].caption
            fields_to_insert = {
                "chat_id": chat_id,
                "media_ids": media_ids,  # Сохраняем массив ID изображений или видео
                "text": caption  # Сохраняем caption как текст
            }
            survey_repo.insert_fields(chat_id, fields_to_insert)
            await bot.send_message(chat_id, MEDIA_SUCCESS, reply_markup=profile_edit_keyboard())
            await state.set_state(Change.profile_change)
        except Exception as e:
            print("Error in handle_mediagroup:", e)
            await state.set_state(Change.survey_media)
            await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=back_keyboard())



@change_router.message(F.text == edit_profile_buttons["button8"], Change.profile_change)
async def edit_profile_back_to_main_menu(message: Message, state: FSMContext):
    await message.answer(BACK_TO_MENU, reply_markup=registered_keyboard())
    await state.set_state(User.registration_end)
