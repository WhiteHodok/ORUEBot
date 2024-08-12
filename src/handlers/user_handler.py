from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from config import bot
from src.keyboards.user_keyboard import (
    user_keyboard_button, user_keyboard, guild_keyboard_button, guild_keyboard
)
from src.phrases import (
    SURVEY_EXAMPLE,
    SURVEY_START_REGISTRATION,
    SURVEY_FIO_EXAMPLE,
    SURVEY_FIO_VALIDATION,
    SURVEY_GUILD_EXAMPLE
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
    chat_id = message.chat.id
    fio = message.text
    if validate_fio(fio):
        await state.update_data(fio=fio)
        await state.set_state(User.registration_handle_guild_start)
        await message.reply(SURVEY_GUILD_EXAMPLE, reply_markup=guild_keyboard())
    else:
        await message.reply(SURVEY_FIO_VALIDATION)
        await state.set_state(User.registration_start)
