from datetime import datetime

from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from cachetools import TTLCache

from database.models import User


class LastUserActivityMiddleware(BaseMiddleware):
    """ Мидлварь, который обновляет раз в день последний онлайн юзера (поле last_user_activity) """
    def __init__(self):
        self.cache = TTLCache(maxsize=10_000, ttl=60*60*24)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        tg_id = event.from_user.id

        if not tg_id in self.cache:
            today = datetime.today()

            username = event.from_user.username
            full_name = event.from_user.full_name

            user = await User.get(tg_id=tg_id)
            user.last_day_online = today
            user.username = username
            user.name = full_name
            await user.save()

            self.cache[tg_id] = None

        return await handler(event, data)
