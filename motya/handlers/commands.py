from aiogram import types

from config import dp, db
from filters.motya_command import MotyaCommand
from utils.message_manager import random_sentence, random_sentence_from_messages, anekdot


@dp.message_handler(MotyaCommand(["анекдот", "анек"]))
async def send_anekdot(message: types.Message):
    sentence = await anekdot()
    await message.reply(sentence) if sentence else None


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
