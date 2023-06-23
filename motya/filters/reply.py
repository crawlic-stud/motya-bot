from typing import List

from aiogram.dispatcher.filters import Filter
from aiogram import types, Bot


class Reply(Filter):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def check(self, message: types.Message) -> bool:
        reply = message.reply_to_message
        if reply is not None and reply.from_id == self.bot.id:
            return True
        return False
