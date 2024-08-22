from aiogram.types import InlineKeyboardButton, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import supabase
import hashlib
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
    "Производство и продажа товаров народного потребления": False,
    "Ремонт и обслуживание техники": False,
    "Разработка и продвижение сайтов": False,
    "Создание и продвижение мобильных приложений": False,
    "Организация мероприятий": False,
    "Консалтинг": False,
    "Обучение и тренинги": False,
    "Туризм": False,
    "Ресторанный бизнес": False,
    "Гостиничный бизнес": False,
    "Транспорт": False,
    "Строительство и ремонт": False,
    "Дизайн интерьеров": False,
    "Юридические услуги": False,
    "Бухгалтерия": False,
    "Медицинские услуги": False,
    "Косметология": False,
    "Фитнес": False,
    "Недвижимость": False,
    "Уход за пожилыми людьми": False,
    "Организация праздников": False,
    "Такси": False,
    "Курьерская доставка": False,
    "Уборка помещений": False,
    "Озеленение и ландшафтный дизайн": False,
    "Установка и обслуживание систем безопасности": False,
    "Разработка и продвижение рекламных кампаний": False,
    "Создание и продвижение видеоконтента": False,
    "Обучение иностранным языкам": False,
    "Подбор персонала": False,
    "Аренда оборудования": False,
    "Прокат автомобилей": False,
    "Доставка продуктов питания": False,
    "Производство и продажа продуктов питания": False,
    "Пошив одежды": False,
    "Изготовление мебели": False,
    "Психологическая помощь": False,
    "Проведение психологических тренингов": False,
    "Предоставление услуг связи": False,
    "Продажа и ремонт компьютерной техники": False,
    "Разработка программного обеспечения": False,
    "Настройка и обслуживание серверов": False,
    "Создание и поддержка веб-сайтов": False,
    "Перевод текстов": False,
    "Написание статей и копирайтинг": False,
    "Создание логотипов и фирменного стиля": False,
    "Фото- и видеосъёмка": False,
    "Организация выставок и ярмарок": False,
    "Организация и продвижение": False
}

def hash_buttons(text):
    return hashlib.md5(text.encode()).hexdigest()[:10]

hash_to_genre = {hash_buttons(genre): genre for genre in genres_of_work.keys()}

def genre_of_work_keyboard():
    kb_builder = InlineKeyboardBuilder()
    for genre, selected in genres_of_work.items():
        callback_data = hash_buttons(genre)  # Используем хеш вместо длинной строки
        kb_builder.add(InlineKeyboardButton(
            text=f"{'✅' if selected else ' '} {genre}",
            callback_data=callback_data
        ))
    kb_builder.adjust(1)  # количество кнопок в строке
    kb_builder.row(InlineKeyboardButton(text="Подтвердить", callback_data="confirm"))
    return kb_builder.as_markup(resize_keyboard=True)


registered_keyboard_buttons = {
    "button1": "📜Моя анкета",
    "button2": "📝Поиск",
}


def registered_keyboard():
    """
    Creates a user keyboard with two buttons.

    Returns:
        ReplyKeyboardMarkup: The user keyboard with two buttons.
    """
    registered_keyboard = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=registered_keyboard_buttons['button1'])

    button2 = KeyboardButton(text=registered_keyboard_buttons['button2'])

    registered_keyboard.row(button1)
    registered_keyboard.row(button2)

    return registered_keyboard.as_markup(resize_keyboard=True)


def skip_keyboard():
    """
    Creates an inline keyboard markup with a single button labeled "Пропустить" (Skip in English).

    Returns:
        InlineKeyboardMarkup: The generated inline keyboard markup.
    """
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="Пропустить", callback_data="skip"))
    return kb_builder.as_markup()



profile_keyboard_buttons = {
    "button1": "📒Изменить анкету",
    "button2": "🔙Назад",
}


def profile_keyboard():
    profile_keyboard = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=profile_keyboard_buttons['button1'])
    button2 = KeyboardButton(text=profile_keyboard_buttons['button2'])
    profile_keyboard.row(button1)
    profile_keyboard.row(button2)
    return profile_keyboard.as_markup(resize_keyboard=True)


edit_profile_buttons = {
    "button1": "📒Изменить ФИО",
    "button2": "📒Изменить Гильдию",
    "button3": "📒Изменить название Компании",
    "button4": "📒Изменить Категории",
    "button5": "📒Изменить Телефон",
    "button6": "📒Изменить Email",
    "button7": "📒Изменить Визитку",
    "button8": "🔙Назад",
}


def profile_edit_keyboard():
    kb_builder = ReplyKeyboardBuilder()
    button1 = KeyboardButton(text=edit_profile_buttons['button1'])
    button2 = KeyboardButton(text=edit_profile_buttons['button2'])
    button3 = KeyboardButton(text=edit_profile_buttons['button3'])
    button4 = KeyboardButton(text=edit_profile_buttons['button4'])
    button5 = KeyboardButton(text=edit_profile_buttons['button5'])
    button6 = KeyboardButton(text=edit_profile_buttons['button6'])
    button7 = KeyboardButton(text=edit_profile_buttons['button7'])
    button8 = KeyboardButton(text=edit_profile_buttons['button8'])
    kb_builder.row(button1, button2)
    kb_builder.row(button3, button4)
    kb_builder.row(button5, button6)
    kb_builder.row(button7, button8)
    return kb_builder.as_markup()


back_button = {
    "button1": "🔙Назад"}


def back_keyboard():
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(KeyboardButton(text=back_button['button1']))
    return kb_builder.as_markup(resize_keyboard=True)


guild_edit_profile = {
    "guild1": "Ⅰ", "guild2": "Ⅱ", "guild3": "Ⅲ", "back1": "🔙Назад"
}


def guild_edit_keyboard():
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(KeyboardButton(text=guild_edit_profile['guild1']), KeyboardButton(text=guild_edit_profile['guild2']),
                   KeyboardButton(text=guild_edit_profile['guild3']))
    kb_builder.row(KeyboardButton(text=guild_edit_profile['back1']))
    return kb_builder.as_markup(resize_keyboard=True)


def reset_genres_of_work():
    for genre in genres_of_work:
        genres_of_work[genre] = False

navigation_keyboard_buttons = {
    "button1": "⬅️Влево",
    "button2": "🔙Назад",
    "button3": "➡️Вправо"
}

def navigation_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text=navigation_keyboard_buttons['button1']),
        KeyboardButton(text=navigation_keyboard_buttons['button2']),
        KeyboardButton(text=navigation_keyboard_buttons['button3'])
    )
    return keyboard.as_markup(resize_keyboard=True)