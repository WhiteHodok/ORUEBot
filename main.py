import asyncio
import logging
import sys

from aiogram.methods import DeleteWebhook

from config import dp, bot
from src.handlers.guest_handler import guest_router
from src.handlers.user_handler import user_router


async def start():
    dp.include_routers(guest_router, user_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
