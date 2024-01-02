import logging
from typing import Any, Awaitable, Callable

from aiogram import types, BaseMiddleware
from filters.motya_command import COMMAND_PREFIX
from models import MessageData
from utils.database import CommonDb


STORE_LIMIT = 5
logger = logging.getLogger("messages")


class MessageSaver(BaseMiddleware):
    def __init__(self, data: dict, database: CommonDb):
        super().__init__()
        self.data = data
        self.database = database

    async def __call__(
        self,
        handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]],
        message: types.Message,
        data: dict[str, Any],
    ):
        msg_text = message.text
        chat_id = message.chat.id
        res = handler(message, data)

        if not message.from_user:
            return await res

        user_id = message.from_user.id

        if chat_id > 0 or msg_text is None:
            return await res

        if not self.data.get(chat_id):
            self.data[chat_id] = []

        # save to temp storage to reduce calls to database
        if not msg_text.lower().startswith(COMMAND_PREFIX):
            self.data[chat_id].append(MessageData(user_id, msg_text))
            logger.info(
                f"Added message from user {user_id} from chat {chat_id} to temporary storage."
            )

        if len(self.data[chat_id]) >= STORE_LIMIT:
            logger.info(
                f"Saved {STORE_LIMIT} messages from chat {chat_id} to database."
            )
            self.database.save_messages(chat_id, self.data[chat_id])
            self.data[chat_id] = []

        return await res
