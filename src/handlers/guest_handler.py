import json
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, WebAppData
from config import bot
from src.keyboards.user_keyboard import *  # TODO
from src.keyboards.guest_keyboard import guest_user_keyboard
from src.phrases import *  # TODO
from src.states.guest_states import Guest
from src.states.user_states import User
from config import supabase

guest_router = Router()


@guest_router.message(CommandStart(), StateFilter(None))
async def start_command(message: Message, state: FSMContext):
    chat_id = message.chat.id

    if supabase.table("UserData").select("chat_id").eq("chat_id", chat_id).execute().data:
        await bot.send_message(chat_id, QUALIFIED_USER_TEXT)
        await state.set_state(User.main)
        return

    await state.set_state(Guest.guest_main_room)
    await bot.send_message(chat_id, CAPTION_QR_TEXT, reply_markup=guest_user_keyboard())


@guest_router.message(F.content_type == 'web_app_data', Guest.guest_main_room)
async def guest_qr(data: WebAppData, state: FSMContext):
    chat_id = data.chat.id
    promocode = data.web_app_data.data
    await check_qr_code(chat_id, promocode, state)


async def check_qr_code(chat_id, promocode, state: FSMContext):
    with open('roles.json') as file:
        roles = json.load(file)
        qr_parameter = roles.get("QR")
        if promocode == qr_parameter:
            await supabase.table("UserData").insert({"chat_id": chat_id}).execute()
            await bot.send_message(chat_id, QUALIFIED_USER_TEXT)
            await state.set_state(User.main)
        else:
            await bot.send_message(chat_id, WRONG_QR_TEXT)
