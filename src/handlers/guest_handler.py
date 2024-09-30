import io
import json
import PIL
import pyzbar.pyzbar
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, WebAppData
from pyasn1_modules.rfc2985 import contentType

from config import bot
from src.keyboards.user_keyboard import user_keyboard, registered_keyboard
from src.keyboards.guest_keyboard import guest_user_keyboard
from src.phrases import (
    CAPTION_QR_TEXT,
    WRONG_QR_TEXT,
    QUALIFIED_USER_TEXT,
    QR_SUCCESS_TEXT

)
from src.states.guest_states import Guest
from src.states.user_states import User
from config import supabase
from PIL import Image

guest_router = Router()


@guest_router.message(CommandStart(), StateFilter(None, User.registration_end, User.main, Guest.guest_main_room))
async def start_command(message: Message, state: FSMContext):
    """
    Handles the start command for guests.

    This function is an asynchronous handler that is triggered when a guest sends the start command. It checks if the guest's chat ID already exists in the "UserData" table of the Supabase database. If it does, it sends a message indicating that the user is already qualified and sets the state to the main user state. If the chat ID does not exist, it sets the state to the guest main room state and sends a message with a caption asking the guest to scan a QR code.

    Parameters:
        message (Message): The message object containing information about the start command.
        state (FSMContext): The finite state machine context.

    Returns:
        None
    """
    chat_id = message.chat.id

    user_data = supabase.table("UserData").select("clicker").eq("chat_id", chat_id).execute().data

    if user_data:
        # Получаем значение 'clicker' из первого элемента
        clicker_value = user_data[0]['clicker']

        # Проверяем, не является ли значение None
        if clicker_value is not None:
            await bot.send_message(chat_id, QUALIFIED_USER_TEXT, reply_markup=registered_keyboard())
            await state.set_state(User.registration_end)

    await state.set_state(Guest.guest_main_room)
    await bot.send_message(chat_id, CAPTION_QR_TEXT, reply_markup=guest_user_keyboard())


@guest_router.message(F.content_type == 'web_app_data', Guest.guest_main_room)
async def guest_qr(data: WebAppData, state: FSMContext):
    """
    A handler for the guest_qr message event.
    Retrieves the chat_id and promocode from the WebAppData object,
    then calls the check_qr_code function with the obtained parameters.

    Parameters:
        data (WebAppData): The WebAppData object containing information related to the event.
        state (FSMContext): The finite state machine context.

    Returns:
        None
    """
    chat_id = data.chat.id
    promocode = data.web_app_data.data
    await check_qr_code(chat_id, promocode, state)


@guest_router.message(Guest.guest_main_room)
async def guest_message_qr(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == 'photo':
        photo_bytes = await bot.download(file=message.photo[-1].file_id, destination=io.BytesIO())
        photo_bytes = photo_bytes.getvalue()

        photo_image = PIL.Image.open(io.BytesIO(photo_bytes))

        qr_code = pyzbar.pyzbar.decode(photo_image)

        if qr_code:
            qr_code = qr_code[0].data.decode()

        await check_qr_code(chat_id, qr_code, state)
    else:
        await bot.send_message(chat_id, WRONG_QR_TEXT)




async def check_qr_code(chat_id, promocode, state: FSMContext):
    """
    Asynchronously checks if the provided QR code is valid for a guest user.

    Args:
        chat_id (int): The chat ID of the guest user.
        promocode (str): The QR code to be checked.
        state (FSMContext): The finite state machine context.

    Returns:
        None

    This function reads the 'roles.json' file to retrieve the QR code parameter. It then compares the provided QR code
    with the retrieved parameter. If they match, it inserts the guest user's chat ID into the 'UserData' table of the
    Supabase database, sends a message indicating that the user is qualified, and sets the state to the main user state.
    If the QR code does not match, it sends a message indicating that the QR code is wrong.

    Note:
        This function assumes that the 'roles.json' file exists in the same directory as the script and contains the
        'QR' parameter.

    """
    with open('roles.json') as file:
        roles = json.load(file)
        qr_parameter = roles.get("QR")
        if promocode == qr_parameter:
            supabase.table("UserData").insert({"chat_id": chat_id}).execute()
            await bot.send_message(chat_id, QR_SUCCESS_TEXT, reply_markup=user_keyboard())
            await state.set_state(User.main)
        else:
            await bot.send_message(chat_id, WRONG_QR_TEXT)
