import asyncio
import logging
from typing import Any, Awaitable, Callable

from aiogram import Bot, types, BaseMiddleware
from utils.database import CommonDb
from utils.message_manager import answer_with_kb, random_sentence
from utils.tools import roll_chance


# TODO: fetch probability from database and store it somewhere
PROBABILITY = 5 / 100
logger = logging.getLogger("sender")


class RandomSender(BaseMiddleware):
    def __init__(self, database: CommonDb, bot: Bot):
        super().__init__()
        self.database = database
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]],
        message: types.Message,
        data: dict[str, Any],
    ):
        current_state = await data["state"].get_state()
        res = handler(message, data)

        if current_state is not None:
            return await res

        if not roll_chance(PROBABILITY):
            return await res

        async def task():
            chat_id = message.chat.id
            messages = self.database.get_messages_from_chat(chat_id)
            sentence = await random_sentence(messages, chat_id, bot=self.bot)
            if sentence:
                await answer_with_kb(message, sentence)
                logger.info(f"Sent random message to chat {chat_id}")

        asyncio.create_task(task())
        return await res
