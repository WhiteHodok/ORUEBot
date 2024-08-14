import json
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
    genres_of_work,
    registered_keyboard,
    registered_keyboard_buttons
)
from src.phrases import (
    COMPANY_NAME,
    EMAIL_ADDRESS,
    EMAIL_SKIP,
    EMAIL_SUCCESS,
    EMAIL_VALIDATION,
    GENRE_OF_WORK,
    GENRE_OF_WORK_VALIDATION,
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
    MEDIA_VALIDATION,
    NOT_INDEFINED
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
from config import supabase

user_router = Router()

user_router.message.middleware(VerificationMiddleware())
user_router.message.middleware(AlbumMiddleware())


def to_input_media(
        message: Message,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = UNSET_PARSE_MODE,
        caption_entities: Optional[List[MessageEntity]] = None,
) -> InputMedia:
    if message.content_type == "photo":
        cls = InputMediaPhoto
        media = message.photo[0].file_id
    elif message.content_type == "video":
        cls = InputMediaVideo
        media = message.video.file_id
    elif message.content_type == "audio":
        cls = InputMediaAudio
        media = message.audio.file_id
    elif message.content_type == "document":
        cls = InputMediaDocument
        media = message.document.file_id
    else:
        raise ValueError(f"Unsupported media type {message.content_type}")
    caption_message = caption or message.caption
    return cls(
        media=media,
        caption=caption or message.caption,
        parse_mode=parse_mode,
        caption_entities=caption_entities or message.caption_entities,
    )


@user_router.message(F.text == user_keyboard_button['button1'], User.main)
async def show_survey_example(message: Message, state: FSMContext):
    """
    This function is an asynchronous handler that is triggered when a user
    selects the 'button1' from the user keyboard. It sends a message with the
    survey example to the user's chat.

    Args:
        message (Message): The message object containing information about the
        button selection.
        state (FSMContext): The finite state machine context.

    Returns:
        None
    """
    # Get the chat ID from the message
    chat_id = message.chat.id

    # Send the survey example to the user's chat
    await bot.send_message(chat_id, SURVEY_EXAMPLE)


@user_router.message(F.text == user_keyboard_button['button2'], User.main)
async def start_survey_registration(message: Message, state: FSMContext):
    """
    Starts the survey registration process.

    Args:
        message (Message): The message object containing information about the button selection.
        state (FSMContext): The finite state machine context.

    Returns:
        None
    """
    # Get the chat ID from the message
    chat_id = message.chat.id

    # Set the state to the registration start state
    await state.set_state(User.registration_start)

    # Reply to the message with the survey start registration text and remove the reply keyboard
    await message.reply(SURVEY_START_REGISTRATION, reply_markup=ReplyKeyboardRemove())

    # Send a message to the user with the FIO example
    await bot.send_message(chat_id, SURVEY_FIO_EXAMPLE)


@user_router.message(User.registration_start)
async def handle_fio_start(message: Message, state: FSMContext):
    """
    Handles the start of the FIO input in the survey registration process.

    Args:
        message (Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context.

    Returns:
        None
    """
    fio = message.text
    if validate_fio(fio):
        await state.update_data(fio=fio)
        await state.set_state(User.registration_handle_guild_start)
        await message.reply(SURVEY_GUILD_EXAMPLE, reply_markup=guild_keyboard())
    else:
        await message.reply(SURVEY_FIO_VALIDATION)
        await state.set_state(User.registration_start)


@user_router.message(User.registration_handle_guild_start, F.text == guild_keyboard_button['guild1'])
async def handle_guild_start_guild1(message: Message, state: FSMContext):
    """
    Handle the start of the guild selection in the survey registration process.

    Args:
        message (Message): The message object containing the user's input.
        state (FSMContext): The finite state machine context.

    Returns:
        None
    """
    try:
        # Get the guild selection from the message
        guild = message.text

        # Update the state with the guild selection
        await state.update_data(guild=guild)

        # Set the state to the end of the guild selection
        await state.set_state(User.registration_handle_guild_end)

        # Send a message to the user with the company name and remove the reply keyboard
        await message.reply(COMPANY_NAME, reply_markup=ReplyKeyboardRemove())

        # Send a message to the user with the skip button and the skip keyboard
        await message.reply(SKIP_BUTTON, reply_markup=skip_keyboard())
    except Exception as e:
        # Print the error if any exception occurs
        print("Error in handle_guild_start:", e)


@user_router.message(User.registration_handle_guild_start, F.text == guild_keyboard_button['guild2'])
async def handle_guild_start_guild2(message: Message, state: FSMContext):
    """
    Handle the start of the guild selection process.

    Args:
        message (Message): The message object.
        state (FSMContext): The finite state machine context.

    Returns:
        None

    Raises:
        Exception: If an error occurs.
    """
    try:
        guild = message.text
        await state.update_data(guild=guild)
        await state.set_state(User.registration_handle_guild_end)
        await message.reply(COMPANY_NAME, reply_markup=ReplyKeyboardRemove())
        await message.reply(SKIP_BUTTON, reply_markup=skip_keyboard())
    except Exception as e:
        print("Error in handle_guild_start:", e)


@user_router.message(User.registration_handle_guild_start, F.text == guild_keyboard_button['guild3'])
async def handle_guild_start_guild3(message: Message, state: FSMContext):
    """
    Handle the start of the guild selection process.

    Args:
        message (Message): The message object.
        state (FSMContext): The finite state machine context.

    Returns:
        None

    Raises:
        Exception: If an error occurs.
    """
    try:
        guild = message.text
        await state.update_data(guild=guild)
        await state.set_state(User.registration_handle_guild_end)
        await message.reply(COMPANY_NAME, reply_markup=ReplyKeyboardRemove())
        await message.reply(SKIP_BUTTON, reply_markup=skip_keyboard())
    except Exception as e:
        print("Error in handle_guild_start:", e)


@user_router.callback_query(User.registration_handle_guild_end, F.data == 'skip')
async def handle_guild_end_skip(call: CallbackQuery, state: FSMContext):
    """
    Handle the skip button in the guild selection process.

    Args:
        call (CallbackQuery): The callback query.
        state (FSMContext): The state of the conversation.

    Returns:
        None

    Raises:
        Exception: If an error occurs.
    """
    try:
        # Get the chat ID
        chat_id = call.message.chat.id

        # Set the company name to 'Не указано'
        company_name = 'Не указано'

        # Update the state with the company name
        await state.update_data(company_name=company_name)

        # Set the state to the genre of work
        await state.set_state(User.registration_handle_genre_of_work)

        # Send a message to the user with the genre of work and the genre of work keyboard
        await bot.send_message(chat_id, GENRE_OF_WORK, reply_markup=genre_of_work_keyboard())
    except Exception as e:
        # Print the error if any exception occurs
        print("Error in handle_guild_end:", e)


@user_router.message(User.registration_handle_guild_end)
async def handle_guild_end(message: Message, state: FSMContext):
    """
    Handle the end of the guild selection process.

    Args:
        message (Message): The message received.
        state (FSMContext): The state of the conversation.

    Returns:
        None

    Raises:
        Exception: If an error occurs.
    """
    try:
        # Get the company name from the message
        company_name = message.text

        # Update the state with the company name
        await state.update_data(company_name=company_name)

        # Set the state to the genre of work
        await state.set_state(User.registration_handle_genre_of_work)

        # Send a message to the user with the genre of work and the genre of work keyboard
        await message.reply(GENRE_OF_WORK, reply_markup=genre_of_work_keyboard())
    except Exception as e:
        # Print the error if any exception occurs
        print("Error in handle_guild_end:", e)


@user_router.callback_query(User.registration_handle_genre_of_work)
async def handle_genre_of_work_start(callback_query: CallbackQuery, state: FSMContext):
    """
    Handle callback query for genre of work.
    """
    try:
        chat_id = callback_query.message.chat.id
        genre = callback_query.data
        selected_genres = [lang for lang, selected in genres_of_work.items() if selected]
        if genre == "confirm" and selected_genres:
            chat_id = callback_query.message.chat.id
            await state.update_data(genres_of_work=selected_genres)
            await bot.send_message(chat_id, CATEGORIES + ", ".join(selected_genres))
            await bot.send_message(chat_id, MEDIA_CAPTION, reply_markup=skip_keyboard())
            await state.set_state(User.registration_handle_photo_survey_start)
        elif genre in genres_of_work:
            genres_of_work[genre] = not genres_of_work[genre]
            await callback_query.message.edit_reply_markup(reply_markup=genre_of_work_keyboard())
        else:
            await bot.send_message(chat_id, GENRE_OF_WORK_VALIDATION)
    except Exception as e:
        print("Error in handle_genre_of_work_start:", e)


@user_router.callback_query(User.registration_handle_photo_survey_start, F.data == 'skip')
async def skip_survey_media(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await state.set_state(User.registration_handle_photo_survey_end)
        supabase.table("Surveys").insert({
            "chat_id": chat_id
        }).execute()
        await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())

    except Exception as e:
        print("Error in handle_guild_end:", e)


@user_router.message(User.registration_handle_photo_survey_start)
async def handle_mediagroup_start(message: Message, state: FSMContext, album: list = None):
    chat_id = message.chat.id
    if album is None:
        content_type = message.content_type
        try:
            match content_type:
                case 'text':
                    supabase.table("Surveys").insert({
                        "chat_id": chat_id,
                        "text": message.text
                    }).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'photo':
                    supabase.table("Surveys").insert({
                        "chat_id": chat_id,
                        "photo_id": message.photo[-1].file_id,  # Сохраняем ID изображения
                        "text": message.caption  # Сохраняем caption как текст
                    }).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'video':
                    supabase.table("Surveys").insert({
                        "chat_id": chat_id,
                        "video_id": message.video.file_id,  # Сохраняем ID видео
                        "text": message.caption  # Сохраняем caption как текст
                    }).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'document':
                    supabase.table("Surveys").insert({
                        "chat_id": chat_id,
                        "document_id": message.document.file_id,  # Сохраняем ID документа
                        "text": message.caption  # Сохраняем caption как текст
                    }).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case _:
                    await state.set_state(User.registration_handle_photo_survey_start)
                    await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=skip_keyboard())
        except Exception as e:
            print("Error in handle_media:", e)
            await state.set_state(User.registration_handle_photo_survey_start)
            await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=skip_keyboard())
    else:
        try:
            media_ids = [content.photo[-1].file_id if content.photo else content.video.file_id for content in album]
            caption = album[0].caption
            supabase.table("Surveys").insert({
                "chat_id": chat_id,
                "media_ids": media_ids,  # Сохраняем массив ID изображений или видео
                "text": caption  # Сохраняем caption как текст
            }).execute()
            await bot.send_message(chat_id, MEDIA_SUCCESS)
            await state.set_state(User.registration_handle_photo_survey_end)
            await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
        except Exception as e:
            print("Error in handle_mediagroup:", e)
            await state.set_state(User.registration_handle_photo_survey_start)
            await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=skip_keyboard())


@user_router.message(User.registration_handle_photo_survey_end)
async def handle_survey_phone_number(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        phone_number = message.text
        if validate_phone_number(phone_number):
            await state.update_data(phone_number=phone_number)
            await bot.send_message(chat_id, PHONE_SUCCESS)
            await state.set_state(User.registration_handle_email_start)
            await bot.send_message(chat_id, EMAIL_ADDRESS, reply_markup=skip_keyboard())
        else:
            await bot.send_message(chat_id, PHONE_NUMBER_VALIDATION)
    except Exception as e:
        print("Error in handle_survey_phone_number:", e)
        await state.set_state(User.registration_handle_photo_survey_end)


@user_router.callback_query(User.registration_handle_photo_survey_end, F.data == 'skip')
async def skip_phone_number(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        phone_number = 'Не указан'
        await state.update_data(phone_number=phone_number)
        await state.set_state(User.registration_handle_email_start)
        await bot.send_message(chat_id, EMAIL_ADDRESS, reply_markup=skip_keyboard())
    except Exception as e:
        print("Error in handle_guild_end:", e)


@user_router.message(User.registration_handle_email_start)
async def handle_email_address(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        email_address = message.text
        if validate_email(email_address):
            await state.update_data(email_address=email_address)
            await bot.send_message(chat_id, EMAIL_SUCCESS)
            data = await state.get_data()
            fio = data.get('fio')
            guild = data.get('guild')
            company_name = data.get('company_name')
            genre_of_work = data.get('genres_of_work')
            phone_number = data.get('phone_number')
            email_address = data.get('email_address')
            if fio and guild and company_name and genre_of_work and phone_number and email_address:
                supabase.table("UserData").upsert({
                    "chat_id": chat_id,
                    "fio": fio,
                    'guild': guild,
                    'company': company_name,
                    'genre_work': genre_of_work,
                    'phone': phone_number,
                    'mail': email_address,
                    'clicker': True
                }).execute()
                await state.set_state(User.registration_end)
                await bot.send_message(chat_id, REGISTRATION_END_ASK, reply_markup=registered_keyboard())
            else:
                await state.set_state(User.registration_start)
                await bot.send_message(chat_id, SURVEY_START_REGISTRATION, reply_markup=None)
        else:
            await bot.send_message(chat_id, EMAIL_VALIDATION)
    except Exception as e:
        print("Error in handle_email_address:", e)
        await state.set_state(User.registration_handle_email_start)

@user_router.callback_query(User.registration_handle_email_start, F.data == 'skip')
async def skip_email_address(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, EMAIL_SKIP)
        data = await state.get_data()
        fio = data.get('fio')
        guild = data.get('guild')
        company_name = data.get('company_name')
        genre_of_work = data.get('genres_of_work')
        phone_number = data.get('phone_number')
        email_address = 'Не указан'
        if fio and guild and company_name and genre_of_work and phone_number and email_address:
            supabase.table("UserData").upsert({
                "chat_id": chat_id,
                "fio": fio,
                'guild': guild,
                'company': company_name,
                'genre_work': genre_of_work,
                'phone': phone_number,
                'mail': email_address,
                'clicker': True
            }).execute()
            await state.set_state(User.registration_end)
            await bot.send_message(chat_id, REGISTRATION_END_ASK, reply_markup=registered_keyboard())
        else:
            await state.set_state(User.registration_start)
            await bot.send_message(chat_id, SURVEY_START_REGISTRATION, reply_markup=None)
    except Exception as e:
        print("Error in skip_email_address:", e)
        await state.set_state(User.registration_handle_email_start)

@user_router.message(F.text == registered_keyboard_buttons["button1"], User.registration_end)
async def show_my_survey(message: Message, state: FSMContext):
    chat_id = message.chat.id
    text_response = supabase.table("UserData").select("fio", "guild", "company", "genre_work", "phone", "mail").eq(
        "chat_id", chat_id).execute().data

    message_text = f"ФИО👨🏻‍💼: {text_response[0]['fio']}\n" \
                   f"Гильдия⚜️: {text_response[0]['guild']}\n" \
                   f"Ваша Компания🏛️: {text_response[0]['company']}\n" \
                   f"Категории🔖: {text_response[0]['genre_work']}\n" \
                   f"Номер телефона📱: {text_response[0]['phone']}\n" \
                   f"Email📧: {text_response[0]['mail']}"

    response = supabase.table("Surveys").select("text", "photo_id", "video_id", "document_id", "media_ids").eq(
        "chat_id", chat_id).execute()
    data = response.data[0]
    if data.get("photo_id"):
        await bot.send_photo(chat_id, photo=data["photo_id"], caption=f"Текст вашей визитки:\n" + data.get("text", "") + f"\n" + message_text)
    elif data.get("video_id"):
        await bot.send_video(chat_id, video=data["video_id"], caption=f"Текст вашей визитки:\n" + data.get("text", "") + f" \n" + message_text)
    elif data.get("document_id"):
        await bot.send_document(chat_id, document=data["document_id"], caption=f"Текст вашей визитки:\n" + data.get("text", "") + f" \n" + message_text)
    elif data.get("media_ids"):
        media_ids = json.loads(data["media_ids"])
        media_group = []
        first_media = InputMediaPhoto(media=media_ids[0], caption= "Текст вашей визитки:" + "\n" + data.get("text", "")  +"\n" + message_text)
        media_group.append(first_media)
        for media_id in media_ids[1:]:
            media_group.append(InputMediaPhoto(media=media_id))
        await bot.send_media_group(chat_id, media=media_group)
    elif data.get("text"):
        await bot.send_message(chat_id, f"\n" +"Текст вашей визитки:" + "\n" + data.get("text", "") + f"\n" + message_text)







