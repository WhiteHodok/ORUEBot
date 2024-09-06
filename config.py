from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings
from supabase import Client, create_client


class EnvSettings(BaseSettings):
    """
    Environment settings.
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class BotSettings(EnvSettings):
    token: str


class SupabaseSettings(EnvSettings):
    supabase_url: str
    supabase_key: str


bot_settings = BotSettings()
supabase_settings = SupabaseSettings()

url: str = supabase_settings.supabase_url
key: str = supabase_settings.supabase_key
supabase: Client = create_client(url, key)

default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=bot_settings.token, default=default)
dp = Dispatcher()
