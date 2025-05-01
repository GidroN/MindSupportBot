from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from constants.button_text import ButtonText
from database.models import User


class CheckUserExistsMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = message.from_user.id

        if not await User.get_or_none(tg_id=user_id):
            if message.text == '/start' or message.text == ButtonText.AGREE_AGREEMENT:
                return await handler(message, data)
            await message.answer('Произошла непредвиденная ошибка.\n'
                                 'Перезапустите бота - /start')
        else:
            return await handler(message, data)
