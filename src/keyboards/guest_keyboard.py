from aiogram.types import InlineKeyboardButton, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import supabase

# Гостевая клавиатура для сканирования QR кода
guest_user_button = {"scan": "📲Отсканировать QR-код"}


def guest_user_keyboard():
    """
    Creates a guest user keyboard with a single button for scanning a QR code.

    Returns:
        ReplyKeyboardMarkup: The guest user keyboard with a single button for scanning a QR code.
    """
    guest_keyboard = ReplyKeyboardBuilder()
    qr_button = KeyboardButton(text=guest_user_button['scan'],
                               web_app=WebAppInfo(url="https://vue-qr-tg-scanner.vercel.app"))
    guest_keyboard.row(qr_button)

    return guest_keyboard.as_markup(resize_keyboard=True)
