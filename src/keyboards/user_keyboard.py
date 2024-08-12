from aiogram.types import InlineKeyboardButton, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import supabase

user_keyboard_button = {"button1": "📜Пример анкеты", "button2": "📝Регистрация"}


def user_keyboard():
    """
    Creates a user keyboard with two buttons.

    Returns:
        ReplyKeyboardMarkup: The user keyboard with two buttons.
    """
    user_keyboard = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=user_keyboard_button['button1'])

    button2 = KeyboardButton(text=user_keyboard_button['button2'])

    user_keyboard.row(button1)
    user_keyboard.row(button2)

    return user_keyboard.as_markup(resize_keyboard=True)


guild_keyboard_button = {"guild1": "Ⅰ", "guild2": "Ⅱ", "guild3": "Ⅲ"}


def guild_keyboard():
    guild_keyboard = ReplyKeyboardBuilder()

    guild1 = KeyboardButton(text=guild_keyboard_button['guild1'])
    guild2 = KeyboardButton(text=guild_keyboard_button['guild2'])
    guild3 = KeyboardButton(text=guild_keyboard_button['guild3'])

    guild_keyboard.row(guild1)
    guild_keyboard.row(guild2)
    guild_keyboard.row(guild3)

    return guild_keyboard.as_markup(resize_keyboard=True)
