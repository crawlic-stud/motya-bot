import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.database import Database
from utils.tools import roll_chance
from utils.markov import generate_random_sentence


PROBABILITY = 20 / 100
logger = logging.getLogger("sender")


class RandomSender(BaseMiddleware):
    def __init__(self, database: Database):
        super().__init__()
        self.database = database
    
    async def on_process_message(self, message: types.Message, data: dict):
        # TODO: fetch probability from database and store in some dict or so
        if not roll_chance(PROBABILITY):
            return
        
        chat_id = message.chat.id
        messages = self.database.get_messages_from_chat(chat_id)
        sentence = generate_random_sentence(messages)    
        await message.answer(sentence)
        logger.info(f"Sent random message to chat {chat_id}")
        