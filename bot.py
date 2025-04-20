import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.redis import RedisStorage
from tortoise import Tortoise

from database.connection import init
from misc.config import BOT_TOKEN, redis_instance
from misc.routers import router


async def main():
    # set up logging config
    logging.basicConfig(level=logging.INFO)

    # init db
    await init()

    # set up bot
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=BOT_TOKEN, default=default)
    storage = RedisStorage(redis_instance)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, close_bot_session=False)
    finally:
        # shutdown bot
        tasks = [dp.storage.close(), Tortoise.close_connections()]
        await asyncio.wait([asyncio.create_task(task) for task in tasks])
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped successfully.')
    except (TelegramNetworkError, ConnectionError, SystemExit) as e:
        logging.warning(f'Bot stopped during and error: {e}')
        exit(1)
