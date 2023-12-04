from aiogram import types
from config import common_db, dp
from filters.motya_command import MotyaCommand
from utils.message_manager import random_sentence_with_start, reply_with_kb


def answer_starts_with(starts):
    async def handler(message: types.Message):
        messages = common_db.get_messages_from_chat(message.chat.id)
        sentence = await random_sentence_with_start(starts, messages, message.chat.id)
        await reply_with_kb(message, sentence) if sentence else None

    return handler


dp.register_message_handler(
    answer_starts_with(["ну", "хз", "супер", "не", "что"]),
    MotyaCommand(["как тебе"], strict=False),
)

dp.register_message_handler(
    answer_starts_with(["так", "вот"]), MotyaCommand(["как"], strict=True)
)

dp.register_message_handler(
    answer_starts_with(["это", "такое"]), MotyaCommand(["что"], strict=True)
)

dp.register_message_handler(
    answer_starts_with(["потому"]), MotyaCommand(["почему"], strict=True)
)
