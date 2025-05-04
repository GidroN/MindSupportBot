from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from constants.button_text import ButtonText
from constants.commands import CommandText
from integrations.yandex_gpt.tools import moderate_text


class ValidateMessageTextMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            message: Message,
            data: Dict[str, Any]
    ) -> Any:

        whitelist = [*ButtonText.get_all_buttons(), *CommandText.get_all_commands()]

        if message.content_type == ContentType.TEXT:
            text = message.text
        else:
            text = message.caption

        # Фильтруем только то те сообщения, которые не являются командами,
        # кнопками или пойманы хендлером, который ловит все сообщения.
        if text and text not in whitelist and data["handler"].callback.__name__ != "handle_all_messages":
            print(text)
            async with ChatActionSender(bot=message.bot, chat_id=message.chat.id, initial_sleep=0.5):
                try:
                    is_flagged = await moderate_text(text=message.text, timeout=20)
                except Exception as e:
                    is_flagged = False
                    await message.bot.send_message(
                        chat_id=511952153,
                        text=f"Траблы с подключением к YaGPT: {e}",
                    )

                if is_flagged:
                    await message.answer("Не используй нецензурную брань. Это некрасиво. Попробуй еще раз.")
                    return

        await handler(message, data)
