from typing import Callable, Awaitable, Dict, Any
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from config import supabase


class VerificationMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        chat_id = event.chat.id
        # Проверка наличия chat_id в таблице UserData
        response = supabase.table("UserData").select("chat_id").eq("chat_id", chat_id).execute()
        user_data = response.data

        # Если chat_id найден, продолжаем обработку
        if user_data and event.chat.id > 0:
            return await handler(event, data)
        else:
            # Иначе отправляем сообщение пользователю
            await event.answer('Вы не являетесь членом союза!')



