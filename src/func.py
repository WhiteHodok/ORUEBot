import json
from aiogram.types import InputMediaPhoto
import supabase
from config import bot
from config import supabase
from src.repo.SurveyRepo import SurveyRepository
from src.repo.UserDataRepo import UserDataRepository

user_repo = UserDataRepository(supabase)
survey_repo = SurveyRepository(supabase)


async def send_profile(bot, chat_id, user):
    try:
        genre_work = json.loads(user['genre_work'].replace("'", '"'))
    except json.JSONDecodeError:
        genre_work = []

    message_text = (
        f"**ФИО👨🏻‍💼:** {user['fio']}\n"
        f"**Гильдия⚜️:** {user['guild']}\n"
        f"**Компания🏛️:** {user['company']}\n"
        f"**Категории🔖:** {', '.join(genre_work)}\n"  
        f"**Номер телефона📱:** {user['phone']}\n"
        f"**Email📧:** {user['mail']}"
    )
    chat_id_user = user['chat_id']
    survey_data = survey_repo.get_user_order_data(chat_id_user)[0]

    if survey_data.get("photo_id"):
        await bot.send_photo(
            chat_id=chat_id,
            photo=survey_data["photo_id"],
            caption=f"**Текст визитки:**\n{survey_data.get('text', '')}\n\n{message_text}" if survey_data.get("text") else message_text,
            parse_mode="Markdown"
        )
    elif survey_data.get("document_id"):
        await bot.send_document(
            chat_id=chat_id,
            document=survey_data["document_id"],
            caption=f"**Текст визитки:**\n{survey_data.get('text', '')}\n\n{message_text}" if survey_data.get("text") else message_text,
            parse_mode="Markdown"
        )
    elif survey_data.get("media_ids"):
        media_ids = json.loads(survey_data["media_ids"])
        media_group = []
        first_media = InputMediaPhoto(
            media=media_ids[0],
            caption=f"**Текст визитки:**\n{survey_data.get('text', '')}\n\n{message_text}" if survey_data.get("text") else message_text,
            parse_mode="Markdown"
        )
        media_group.append(first_media)
        for media_id in media_ids[1:]:
            media_group.append(InputMediaPhoto(media=media_id))
        await bot.send_media_group(chat_id=chat_id, media=media_group)
    elif survey_data.get("text"):
        await bot.send_message(
            chat_id=chat_id,
            text=f"**Текст визитки:**\n{survey_data.get('text', '')}\n\n{message_text}",
            parse_mode="Markdown"
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"Визитка отсутствует\n\n{message_text}",
            parse_mode="Markdown"
        )
