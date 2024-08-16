import json
from aiogram.types import InputMediaPhoto
import supabase
from config import bot
from config import supabase

async def send_profile(bot, chat_id, user):
    message_text = (
        f"**ФИО👨🏻‍💼:** {user['fio']}\n"
        f"**Гильдия⚜️:** {user['guild']}\n"
        f"**Компания🏛️:** {user['company']}\n"
        f"**Категории🔖:** {user['genre_work']}\n"
        f"**Номер телефона📱:** {user['phone']}\n"
        f"**Email📧:** {user['mail']}"
    )
    survey_response = supabase.table("Surveys").select("text, photo_id, video_id, document_id, media_ids").eq("chat_id", user['chat_id']).execute()
    survey_data = survey_response.data[0]

    if survey_data.get("photo_id"):
        await bot.send_photo(
            chat_id=chat_id,
            photo=survey_data["photo_id"],
            caption=f"**Текст визитки:**\n{survey_data.get('text', '')}\n\n{message_text}" if survey_data.get("text") else message_text,
            parse_mode="Markdown"
        )
    elif survey_data.get("video_id"):
        await bot.send_video(
            chat_id=chat_id,
            video=survey_data["video_id"],
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
