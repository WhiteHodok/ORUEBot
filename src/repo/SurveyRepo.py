from postgrest import APIResponse
from supabase import Client, create_client
from typing import Optional, Any


class SurveyRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def insert_field(self, chat_id: int, field: str, value: str or list or bool):
        """Вставить указанное значение в указанное поле в таблице Surveys"""
        self.supabase.table("Surveys").insert({"chat_id": chat_id, field: value}).execute()

    def insert_fields(self, chat_id: int, fields: dict):
        """Вставить указанное значение в указанные поля в таблице Surveys"""
        self.supabase.table("Surveys").insert({"chat_id": chat_id, **fields}).execute()

    def update_field(self, chat_id: int, field: str, value: str or list):
        """Обновить указанное значение в указанном поле в таблице Surveys"""
        self.supabase.table("Surveys").update({field: value}).eq("chat_id", chat_id).execute()

    def update_fields(self, chat_id: int, fields: dict):
        """Обновить указанное значение в указанные поля в таблице Surveys"""
        self.supabase.table("Surveys").update({**fields}).eq("chat_id", chat_id).execute()

    def delete_user_data(self, chat_id: int):
        """Удалить все данные пользователя по chat_id"""
        self.supabase.table("Surveys").delete().eq("chat_id", chat_id).execute()

    def get_user_order_data(self, chat_id: int):
        """Получить все данные пользователя по chat_id"""
        response = self.supabase.table("Surveys").select("chat_id").eq("chat_id", chat_id).execute()
        return response.data


