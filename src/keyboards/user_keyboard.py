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
    """
    Creates a reply keyboard with three guild buttons.

    Returns:
        InlineKeyboardMarkup: The reply keyboard.
    """
    # Create a new ReplyKeyboardBuilder
    guild_keyboard = ReplyKeyboardBuilder()

    # Create three KeyboardButton objects with the guild button texts
    guild1 = KeyboardButton(text=guild_keyboard_button['guild1'])
    guild2 = KeyboardButton(text=guild_keyboard_button['guild2'])
    guild3 = KeyboardButton(text=guild_keyboard_button['guild3'])

    # Add the guild buttons to a new row in the reply keyboard
    guild_keyboard.row(guild1, guild2, guild3)

    # Return the reply keyboard as a markup
    return guild_keyboard.as_markup(resize_keyboard=True)


genres_of_work = {
    "Java": False, "Scala": False, "Python": False,
    "C#": False, "C/C++": False, "Golang": False,
    "Ruby": False, "PHP": False, "Node.js": False,
    "Solidity": False, "Web Frontend": False,
    "Vue": False, "Angular": False, "React": False,
    "iOS": False, "Android": False, "Flutter": False,
    "React Native": False,
}


def genre_of_work_keyboard():
    """
    Generates an inline keyboard markup for selecting genres of work.

    Returns:
        InlineKeyboardMarkup: The generated inline keyboard markup.
    """
    kb_builder = InlineKeyboardBuilder()
    for language, selected in genres_of_work.items():
        kb_builder.add(InlineKeyboardButton(
            text=f"{'✅' if selected else ' '} {language}",
            callback_data=language
        ))
    kb_builder.adjust(3)  # количество кнопок в строке
    kb_builder.row(InlineKeyboardButton(text="Подтвердить", callback_data="confirm"))
    return kb_builder.as_markup()


def skip_keyboard():
    """
    Creates an inline keyboard markup with a single button labeled "Пропустить" (Skip in English).

    Returns:
        InlineKeyboardMarkup: The generated inline keyboard markup.
    """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="Пропустить", callback_data="skip"))
    return kb_builder.as_markup()
