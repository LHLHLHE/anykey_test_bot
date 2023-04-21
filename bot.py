import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import handlers

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
OPEN_WEATHER_API_KEY = os.getenv('OPEN_WEATHER_API_KEY')
EXCHANGERATES_API_KEY = os.getenv('EXCHANGERATES_API_KEY')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Здесь хранятся id групповых чатов, в которые добален бот
group_chats = {}


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
