from postgrest import APIResponse
from supabase import Client, create_client
from typing import Optional, Any



class UserDataRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    def insert_field(self, chat_id: int, field: str, value: str or list or bool):
        """Вставить указанное значение в указанное поле в таблице UserData"""
        self.supabase.table("UserData").insert({"chat_id": chat_id, field: value}).execute()

    def update_field(self, chat_id: int, field: str, value: str or list):
        """Обновить указанное значение в указанном поле в таблице UserData"""
        self.supabase.table("UserData").update({field: value}).eq("chat_id", chat_id).execute()

    def get_user_by_chat_id(self, chat_id: int) -> APIResponse[Any]:
        """Получить данные пользователя по chat_id"""
        return self.supabase.table("UserData").select("*").eq("chat_id", chat_id).execute()

    def delete_all_user_data(self, chat_id: int):
        """Удалить все данные пользователя по chat_id"""
        self.supabase.table("UserData").delete().eq("chat_id", chat_id).execute()
        self.supabase.table("Surveys").delete().eq("chat_id", chat_id).execute()

    def get_all_users(self) -> APIResponse[Any]:
        """Получить список всех пользователей с нужными полями"""
        return self.supabase.table("UserData").select("fio, guild, company, genre_work, phone, mail, chat_id").execute()

