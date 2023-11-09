import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.database import Database
from filters.motya_command import COMMAND_PREFIX
from models import MessageData


STORE_LIMIT = 5
logger = logging.getLogger("messages")


class MessageSaver(BaseMiddleware):
    def __init__(self, data: dict, database: Database):
        super().__init__()
        self.data = data
        self.database = database

    async def on_pre_process_message(self, message: types.Message, data: dict):
        msg_text = message.text
        chat_id = message.chat.id
        user_id = message.from_id

        if chat_id > 0 or msg_text is None:
            return

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
