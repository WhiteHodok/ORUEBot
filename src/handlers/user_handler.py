from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from config import bot
from src.keyboards.user_keyboard import (
    genre_of_work_keyboard,
    skip_keyboard,
    user_keyboard_button,
    user_keyboard,
    guild_keyboard_button,
    guild_keyboard,
    genres_of_work
)
from src.phrases import (
    COMPANY_NAME,
    GENRE_OF_WORK,
    SURVEY_EXAMPLE,
    SURVEY_EXAMPLE_ERROR,
    SURVEY_START_REGISTRATION,
    SURVEY_FIO_EXAMPLE,
    SURVEY_FIO_VALIDATION,
    SURVEY_GUILD_EXAMPLE,
    SKIP_BUTTON
)
from src.states.user_states import User
from src.middlewares.user_verification_middleware import VerificationMiddleware
from src.handlers.user_validation import (
    validate_fio
)
from config import supabase

user_router = Router()

user_router.message.middleware(VerificationMiddleware())


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
            selected_genres = [lang for lang, selected in genres_of_work.items() if selected]
            await state.update_data(genres_of_work=selected_genres)
        elif genre in genres_of_work:
            genres_of_work[genre] = not genres_of_work[genre]
            await callback_query.message.edit_reply_markup(reply_markup=genre_of_work_keyboard())
    except Exception as e:
        print("Error in handle_genre_of_work_start:", e)
