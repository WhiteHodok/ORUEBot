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
        genre = callback_query.data
        if genre == "confirm":
            chat_id = callback_query.message.chat.id
            selected_genres = [lang for lang, selected in genres_of_work.items() if selected]
            await state.update_data(genres_of_work=selected_genres) #TODO Можно ничего не выбирать и нажать подтвердить, надо пофиксить
            await bot.send_message(chat_id, CATEGORIES + ", ".join(selected_genres))
            await bot.send_message(chat_id, MEDIA_CAPTION, reply_markup=skip_keyboard()) 
            await state.set_state(User.registration_handle_photo_survey_start)
        elif genre in genres_of_work:
            genres_of_work[genre] = not genres_of_work[genre]
            await callback_query.message.edit_reply_markup(reply_markup=genre_of_work_keyboard())
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
                        "message_id": message.message_id,
                        "text": message.text
                    }).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'photo':
                    supabase.table("Surveys").insert({
                        "text": message.caption,
                        "chat_id": chat_id,
                        "message_id": message.message_id}).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'video':
                    supabase.table("Surveys").insert({
                        "text": message.caption,
                        "chat_id": chat_id,
                        "message_id": message.message_id}).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'document':
                    supabase.table("Surveys").insert({
                        "text": message.caption,
                        "chat_id": chat_id,
                        "message_id": message.message_id}).execute()
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case _:
                    await state.set_state(User.registration_handle_photo_survey_start)
                    await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=skip_keyboard())
        except Exception as e:
            print("Error in handle_mediagroup_start:", e)
            await state.set_state(User.registration_handle_photo_survey_start)
            await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=skip_keyboard())       
    else:
        try:
            media = list()
            caption = album[0].caption
            media.append(to_input_media(album[0], caption))
            for content in range(1, len(album)):
                media.append(to_input_media(message=album[content]))
            supabase.table("Surveys").insert({
                "text": caption,
                "chat_id": chat_id,
                'message_id': message.message_id
            }).execute()
            await bot.send_message(chat_id, MEDIA_SUCCESS)
            await state.set_state(User.registration_handle_photo_survey_end)
            await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
        except Exception as e:
            print("Error in handle_mediagroup_start:", e)
            await state.set_state(User.registration_handle_photo_survey_start)
            await bot.send_message(chat_id, MEDIA_VALIDATION, reply_markup=skip_keyboard())
        except:
            try:
                media = list()
                caption = album[0].caption
                media.append(to_input_media(album[0], caption))
                for content in range(1, len(album)):
                    media.append(to_input_media(message=album[content]))
                supabase.table("Surveys").insert({
                    "text": caption,
                    "chat_id": chat_id,
                    'message_id': message.message_id
                }).execute()
                await bot.send_message(chat_id, MEDIA_SUCCESS)
                await state.set_state(User.registration_handle_photo_survey_end)
                await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
            except Exception as e:
                print("Error in handle_mediagroup_start:", e)
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
        phone_number = '0'
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
                message_text = (
                    f"{REGISTRATION_END_ASK}\n\n"
                    f"Ваше ФИО: {fio}\n"
                    f"Ваша Гильдия: {guild}\n"
                    f"Ваша Компания: {company_name}\n" #TODO Разобраться с визиткой, надо её вывести и потом иметь возможность отредачить
                    f"Ваши категории: {genre_of_work}\n"
                    f"Ваш номер телефона: {phone_number}\n"
                    f"Ваш Email: {email_address}"
                )
                await bot.send_message(chat_id, message_text, reply_markup=registration_edit_keyboard())
                await state.set_state(User.registration_end)
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
        email_adress = 'Не указан'
        if fio and guild and company_name and genre_of_work and phone_number and email_adress:
            message_text = (
                f"{REGISTRATION_END_ASK}\n\n"
                f"Ваше ФИО: {fio}\n"
                f"Ваша Гильдия: {guild}\n"
                f"Ваша Компания: {company_name}\n"
                f"Ваши категории: {genre_of_work}\n"
                f"Ваш номер телефона: {phone_number}\n" #TODO Разобраться с визиткой, надо её вывести и потом иметь возможность отредачить
                f"Ваш Email: {email_adress}"
            )
            await bot.send_message(chat_id, message_text, reply_markup=registration_edit_keyboard())
            await state.set_state(User.registration_end)
        else:
            await state.set_state(User.registration_start)
            await bot.send_message(chat_id, SURVEY_START_REGISTRATION, reply_markup=None)
    except Exception as e:
        print("Error in skip_email_address:", e)
        await state.set_state(User.registration_handle_email_start)

@user_router.callback_query(User.registration_end, F.data == 'confirm')
async def confirm_registration(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        data = await state.get_data()
        fio = data.get('fio')
        guild = data.get('guild')
        company_name = data.get('company_name')
        genre_of_work = data.get('genres_of_work')
        phone_number = data.get('phone_number')
        email_adress = 'Не указан'
        supabase.table("UserData").upsert({
                    "chat_id":chat_id,
                    "fio": fio,
                    'guild': guild,
                    'company': company_name,
                    'genre_work': genre_of_work,
                    'phone': phone_number,
                    'mail': email_adress
                }).execute()
        # await bot.send_message(chat_id, REGISTRATION_END, reply_markup=main_keyboard()) #TODO Main menu keyboard + edit profile 
    except Exception as e:
        print("Error in confirm_registration:", e)
@user_router.callback_query(User.registration_end, F.data == 'edit_fio')
async def edit_registration_fio(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, "ИЗМЕНИТЬ ИМЯ", reply_markup=skip_keyboard()) #TODO: добавить редактирование ФИО
    except Exception as e:
        print("Error in edit_registration:", e)

@user_router.callback_query(User.registration_end, F.data == 'edit_guild')
async def edit_registration_guild(call: CallbackQuery, state: FSMContext):        
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, "ИЗМЕНИТЬ ГИЛЬДИЮ", reply_markup=skip_keyboard()) #TODO: добавить редактирование Гильдии
    except Exception as e:
        print("Error in edit_registration:", e)

@user_router.callback_query(User.registration_end, F.data == 'edit_company')
async def edit_registration_company(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, "ИЗМЕНИТЬ КОМПАНИЮ", reply_markup=skip_keyboard()) #TODO: добавить редактирование Компании
    except Exception as e:
        print("Error in edit_registration:", e)

@user_router.callback_query(User.registration_end, F.data == 'edit_genre_of_work')
async def edit_registration_genre_of_work(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, "ИЗМЕНИТЬ КАТЕГОРИИ", reply_markup=genre_of_work_keyboard()) #TODO: добавить редактирование Категории
    except Exception as e:
        print("Error in edit_registration:", e)

@user_router.callback_query(User.registration_end, F.data == 'edit_phone_number')
async def edit_registration_phone_number(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, "ИЗМЕНИТЬ ТЕЛЕФОН", reply_markup=skip_keyboard()) #TODO: добавить редактирование Телефона
    except Exception as e:
        print("Error in edit_registration:", e)

@user_router.callback_query(User.registration_end, F.data == 'edit_email_address') 
async def edit_registration_email_address(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await bot.send_message(chat_id, "ИЗМЕНИТЬ EMAIL", reply_markup=skip_keyboard()) #TODO: добавить редактирование Email
    except Exception as e:
        print("Error in edit_registration:", e)