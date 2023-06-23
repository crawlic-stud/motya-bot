from aiogram import types

from config import dp, db, motya
from filters.motya_command import MotyaCommand
from filters.reply import Reply
from utils.message_manager import (
    random_sentence, 
    random_sentence_from_messages, 
    random_anekdot,
)


@dp.message_handler(MotyaCommand(["анекдот", "анек"], strict=True))
async def send_anekdot(message: types.Message):
    anekdot = await random_anekdot(3) or await random_anekdot(2)
    await message.reply(anekdot) if anekdot else await message.reply("пшл нх")


@dp.message_handler(MotyaCommand(["паста"], strict=True))
async def send_pasta(message: types.Message):
    pastas = db.get_pastas()
    sentence = await random_sentence_from_messages(pastas)
    if not sentence:
        await message.reply("не получилось...")
        return
    await message.reply(sentence)


@dp.message_handler(MotyaCommand([""]))
async def send_random_message(message: types.Message):
    messages = db.get_messages_from_chat(message.chat.id)
    sentence = await random_sentence(messages, message.chat.id)
    if not sentence:
        # await message.answer("я еще недостаточно у вас научился :(")
        return
    await message.answer(sentence)


@dp.message_handler(Reply(bot=motya))
async def answer_more(message: types.Message):
    return await send_random_message(message)
