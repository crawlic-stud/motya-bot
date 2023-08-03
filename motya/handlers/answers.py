from aiogram import types

from config import dp, db
from filters.motya_command import MotyaCommand

from utils.message_manager import random_sentence_with_start


def answer_starts_with(starts):
    async def handler(message: types.Message):
        messages = db.get_messages_from_chat(message.chat.id)
        sentence = await random_sentence_with_start(starts, messages, message.chat.id)
        await message.reply(sentence) if sentence else None
    return handler


dp.register_message_handler(
    answer_starts_with(["ну", "хз", "супер", "не", "что"]), 
    MotyaCommand(["как тебе"], strict=False)
) 

dp.register_message_handler(
    answer_starts_with(["так", "вот"]), 
    MotyaCommand(["как"], strict=True)
) 

dp.register_message_handler(
    answer_starts_with(["это", "такое"]), 
    MotyaCommand(["что"], strict=True)
) 

dp.register_message_handler(
    answer_starts_with(["потому"]), 
    MotyaCommand(["почему"], strict=True)
) 
