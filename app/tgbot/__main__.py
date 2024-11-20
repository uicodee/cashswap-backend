import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from app.config import load_config
from app.tgbot import handlers

dp = Dispatcher()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    bot = Bot(token=config.tgbot.token, default=DefaultBotProperties(parse_mode="HTML"))
    handlers.setup(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
