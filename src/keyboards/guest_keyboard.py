from aiogram.types import InlineKeyboardButton, WebAppInfo, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from config import supabase

# Гостевая клавиатура для сканирования QR кода
guest_user_button = {"scan": "📲Отсканировать QR-код"}


def guest_user_keyboard():
    guest_keyboard = ReplyKeyboardBuilder()
    qr_button = KeyboardButton(text=guest_user_button['scan'],
                               web_app=WebAppInfo(url="https://vue-qr-tg-scanner.vercel.app"))
    guest_keyboard.row(qr_button)

    return guest_keyboard.as_markup(resize_keyboard=True)
