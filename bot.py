import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from tortoise import Tortoise

from database.connection import init_database
from misc.config import BOT_TOKEN, REDIS_HOST, REDIS_PORT
from middlewares.user_exists import CheckUserExistsMiddleware
from middlewares.validate_message_text import ValidateMessageTextMiddleware
from middlewares.throttling import ThrottlingMiddleware
from misc.routers import router


async def main():
    # set up logging config
    logging.basicConfig(level=logging.INFO)

    # init db
    await init_database()

    # set up bot
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=BOT_TOKEN, default=default)
    redis_instance = Redis(host=REDIS_HOST, port=int(REDIS_PORT))
    storage = RedisStorage(redis_instance)
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    # set up middlewares
    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.message.outer_middleware(CheckUserExistsMiddleware())
    dp.message.middleware(ValidateMessageTextMiddleware())

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
    except ConnectionError:
        logging.info("Error during connecting to redis")
        exit(1)
    except (TelegramNetworkError, SystemExit) as e:
        logging.warning(f'Bot stopped during and error: {e}')
        exit(1)
