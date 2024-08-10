from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from config import bot
from src.keyboards.user_keyboard import *  # TODO
from src.phrases import * #TODO
from src.states.user_states import User
from config import supabase

user_router = Router()