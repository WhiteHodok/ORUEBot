import json
from aiogram import Router, F
from typing import Optional, List, Union, Iterator, Any, Dict, cast
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, MessageEntity, UNSET_PARSE_MODE, InputMedia, \
    InputMediaPhoto, InputMediaAudio, InputMediaVideo, InputMediaDocument
from config import bot

from src.repo.SurveyRepo import SurveyRepository
from src.repo.UserDataRepo import UserDataRepository
from src.func import send_profile
from src.keyboards.user_keyboard import (
    back_keyboard,
    genre_of_work_keyboard,
    hash_buttons,
    navigation_keyboard,
    profile_edit_keyboard,
    profile_keyboard,
    reset_genres_of_work,
    skip_keyboard,
    user_keyboard_button,
    user_keyboard,
    guild_keyboard_button,
    guild_keyboard,
    genres_of_work,
    registered_keyboard,
    registered_keyboard_buttons,
    profile_keyboard_buttons,
    back_button,
    hash_to_genre
)
from src.phrases import (
    BACK_TO_MENU,
    COMPANY_NAME,
    EDIT_PROFILE,
    EMAIL_ADDRESS,
    EMAIL_SKIP,
    EMAIL_SUCCESS,
    EMAIL_VALIDATION,
    GENRE_OF_WORK,
    GENRE_OF_WORK_VALIDATION,
    PHONE_NUMBER_VALIDATION,
    PHONE_SUCCESS,
    PROFILE,
    REGISTRATION_END_ASK,
    SEARCH,
    SEARCH_MENU,
    SEARCH_RESULTS,
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

user_repo = UserDataRepository(supabase)
survey_repo = SurveyRepository(supabase)

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
                await bot.send_message(chat_id, MEDIA_CAPTION, reply_markup=skip_keyboard())
                reset_genres_of_work()
                await state.set_state(User.registration_handle_photo_survey_start)
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



@user_router.callback_query(User.registration_handle_photo_survey_start, F.data == 'skip')
async def skip_survey_media(call: CallbackQuery, state: FSMContext):
    try:
        chat_id = call.message.chat.id
        await state.set_state(User.registration_handle_photo_survey_end)
        user_repo.insert_field(chat_id, "chat_id", chat_id)
        survey_repo.insert_field(chat_id, "chat_id", chat_id)
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
                    survey_repo.insert_field(chat_id, "text", message.text)
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'photo':
                    
                    survey_repo.insert_field(chat_id, "photo_id", message.photo[-1].file_id)
                    survey_repo.update_field(chat_id, "text", message.caption)
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'video':
                    survey_repo.insert_field(chat_id, "video_id", message.video.file_id)
                    survey_repo.update_field(chat_id, "text", message.caption)
                    await bot.send_message(chat_id, MEDIA_SUCCESS)
                    await state.set_state(User.registration_handle_photo_survey_end)
                    await bot.send_message(chat_id, SURVEY_PHONE_NUMBER, reply_markup=skip_keyboard())
                case 'document':
                    survey_repo.insert_field(chat_id, "document_id", message.document.file_id)
                    survey_repo.update_field(chat_id, "text", message.caption)
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
            survey_repo.insert_field(chat_id, "media_ids", media_ids)
            survey_repo.update_field(chat_id, "text", caption)
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
                user_repo.update_field(chat_id, "fio", fio)
                user_repo.update_field(chat_id, "guild", guild)
                user_repo.update_field(chat_id, "company", company_name)
                user_repo.update_field(chat_id, "genre_work", genre_of_work)
                user_repo.update_field(chat_id, "phone", phone_number)
                user_repo.update_field(chat_id, "mail", email_address)
                user_repo.update_field(chat_id, "clicker", True)
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
async def skip_email_address_handler(call: CallbackQuery, state: FSMContext):
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
            user_repo.update_field(chat_id, "fio", fio)
            user_repo.update_field(chat_id, "guild", guild)
            user_repo.update_field(chat_id, "company", company_name)
            user_repo.update_field(chat_id, "genre_work", genre_of_work)
            user_repo.update_field(chat_id, "phone", phone_number)
            user_repo.update_field(chat_id, "mail", email_address)
            user_repo.update_field(chat_id, "clicker", True)
            await state.set_state(User.registration_end)
            await bot.send_message(chat_id, REGISTRATION_END_ASK, reply_markup=registered_keyboard())
        else:
            await state.set_state(User.registration_start)
            await bot.send_message(chat_id, SURVEY_START_REGISTRATION, reply_markup=None)
    except Exception as e:
        print("Error in skip_email_address:", e)
        await state.set_state(User.registration_handle_email_start)


@user_router.message(F.text == registered_keyboard_buttons["button1"], User.registration_end)
async def show_my_survey_handler(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        await bot.send_message(chat_id, PROFILE, reply_markup=profile_keyboard())

        text_response = user_repo.get_user_by_chat_id(chat_id)
        user_data = text_response.data[0]
        genre_work = json.loads(user_data['genre_work']) if user_data.get('genre_work') else []
        message_text = f"ФИО👨🏻‍💼: {user_data['fio']}\n" \
                   f"Гильдия⚜️: {user_data['guild']}\n" \
                   f"Ваша Компания🏛️: {user_data['company']}\n" \
                   f"Категории🔖: {', '.join(genre_work)}\n" \
                   f"Номер телефона📱: {user_data['phone']}\n" \
                   f"Email📧: {user_data['mail']}"

        response_media = survey_repo.get_user_order_data(chat_id)
        data = response_media[0]
        if data.get("photo_id"):
            await bot.send_photo(
                chat_id,
                photo=data["photo_id"],
                caption=f"Текст вашей визитки:\n{data.get('text', '')}\n{message_text}" if data.get("text") else message_text
            )
            await state.set_state(User.profile)
        elif data.get("video_id"):
            await bot.send_video(
                chat_id,
                video=data["video_id"],
                caption=f"Текст вашей визитки:\n{data.get('text', '')}\n{message_text}" if data.get("text") else message_text
            )
            await state.set_state(User.profile)
        elif data.get("document_id"):
            await bot.send_document(
                chat_id,
                document=data["document_id"],
                caption=f"Текст вашей визитки:\n{data.get('text', '')}\n{message_text}" if data.get("text") else message_text
            )
            await state.set_state(User.profile)
        elif data.get("media_ids"):
            media_ids = json.loads(data["media_ids"])
            media_group = []
            # Добавляем первый элемент с подписью, если текст есть
            first_media = InputMediaPhoto(
                media=media_ids[0],
                caption=f"Текст вашей визитки:\n{data.get('text', '')}\n{message_text}" if data.get("text") else message_text
            )
            await state.set_state(User.profile)
            media_group.append(first_media)
            for media_id in media_ids[1:]:
                media_group.append(InputMediaPhoto(media=media_id))
            await bot.send_media_group(chat_id, media=media_group)
            await state.set_state(User.profile)
        elif data.get("text"):
            await bot.send_message(chat_id, f"\n" + "Текст вашей визитки:" + "\n" + data.get("text", "") + f"\n" + message_text)
            await state.set_state(User.profile)
    except Exception as e:
        print("Error in show_my_survey_handler:", e)

@user_router.message(F.text == profile_keyboard_buttons["button1"], User.profile)
async def edit_profile_handler(message: Message, state: FSMContext):
    await message.answer(EDIT_PROFILE, reply_markup=profile_edit_keyboard())
    await state.set_state(Change.profile_change)

@user_router.message(F.text == profile_keyboard_buttons["button2"], User.profile)
async def back_to_menu_from_profile(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        await bot.send_message(chat_id, BACK_TO_MENU, reply_markup=registered_keyboard())
        await state.set_state(User.registration_end)
    except Exception as e:
        print("Error in back_to_menu_from_profile:", e)

@user_router.message(F.text == registered_keyboard_buttons["button2"], User.registration_end)
async def search_button_handler(message: Message, state: FSMContext):
    try:
        chat_id = message.chat.id
        await bot.send_message(chat_id, SEARCH_MENU, reply_markup=back_keyboard())
        await message.answer(SEARCH, reply_markup=genre_of_work_keyboard())
        await state.set_state(User.search)
    except Exception as e:
        print("Error in search_button_handler:", e)

@user_router.message(F.text == back_button['button1'], User.search)
async def edit_profile_back(message: Message, state: FSMContext):
    await message.answer(BACK_TO_MENU,reply_markup=registered_keyboard()) 
    reset_genres_of_work()
    await state.set_state(User.registration_end)


@user_router.callback_query(User.search)
async def search_handler(callback_query: CallbackQuery, state: FSMContext):
    try:
        chat_id = callback_query.message.chat.id
        genre_hash = callback_query.data
        selected_genres = [genre for genre, selected in genres_of_work.items() if selected]

        if genre_hash == "confirm":
            if selected_genres:
                
                response = user_repo.get_all_users()
                users = response.data if response.data else []

                if users:
                    def genre_match_count(user):
                        try:
                            user_genres = json.loads(user['genre_work'].replace("'", '"'))
                        except json.JSONDecodeError:
                            user_genres = []

                        match_count = len(set(selected_genres) & set(user_genres))
                        print(f"{user['fio']}: {match_count} matches with {user_genres}")
                        return match_count

                    filtered_users = [user for user in users if genre_match_count(user) > 0 and user['chat_id'] != chat_id] 

                    sorted_users = sorted(
                        filtered_users,
                        key=lambda user: (
                            user['guild'], 
                            -genre_match_count(user)
                        )
                    )

                    if sorted_users:
                        await state.update_data(sorted_users=sorted_users, current_index=0)
                        await send_profile(bot, chat_id, sorted_users[0])
                        await bot.send_message(chat_id, "Используйте кнопки для навигации.", reply_markup=navigation_keyboard())
                        await state.set_state(User.search_active)
                    else:
                        await bot.send_message(chat_id, "Нет пользователей, соответствующих выбранным критериям.")
                else:
                    await bot.send_message(chat_id, "Нет пользователей, соответствующих выбранным критериям.")
            else:
                await callback_query.answer("Выберите хотя бы одну категорию!", show_alert=True)
        elif genre_hash in hash_to_genre:
            genre = hash_to_genre[genre_hash]
            genres_of_work[genre] = not genres_of_work[genre]
            await callback_query.message.edit_reply_markup(reply_markup=genre_of_work_keyboard())
        else:
            await callback_query.answer("Выберите корректную категорию", show_alert=True)
    except Exception as e:
        print("Error in handling genre selection:", e)

@user_router.message(User.search_active)
async def navigate_profiles(message: Message, state: FSMContext):
    data = await state.get_data()
    sorted_users = data.get('sorted_users', [])
    current_index = data.get('current_index', 0)

    if not sorted_users:
        await message.answer("Нет доступных анкет.")
        return
    
    if message.text == "⬅️Влево":
        current_index = (current_index - 1) % len(sorted_users)
    elif message.text == "➡️Вправо":
        current_index = (current_index + 1) % len(sorted_users)
    else: 
        await state.set_state(User.registration_end)
        reset_genres_of_work()
        await message.answer("Вы вернулись назад.", reply_markup=registered_keyboard())
        return
    
    await state.update_data(current_index=current_index)
    await send_profile(bot, message.chat.id, sorted_users[current_index])


#чтоб своя не выводилась  фикс багов от Влада