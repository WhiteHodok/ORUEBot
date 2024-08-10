from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings
from supabase import Client, create_client


class Secrets(BaseSettings):
    token: str
    #admin_id: int
    supabase_url: str
    supabase_key: str
    #redis_url: str
    #group_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


secrets = Secrets()

# init supabase
url: str = secrets.supabase_url
key: str = secrets.supabase_key
supabase: Client = create_client(url, key)

#group_id = secrets.group_id

default = DefaultBotProperties(parse_mode='Markdown', protect_content=False)
bot = Bot(token=secrets.token, default=default)
dp = Dispatcher()
