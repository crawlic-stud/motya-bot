import asyncio

from aiogram import types

from config import dp, db
from filters.motya_command import MotyaCommand
from utils.markov import generate_random_sentence


@dp.message_handler(MotyaCommand([""]))
async def send_random_message(message: types.Message):
    
    async def task():
        messages = db.get_messages_from_chat(message.chat.id)
        sentence = generate_random_sentence(messages)
        if not sentence:
            await message.answer("я еще недостаточно у вас научился :(")
            return
        await message.answer(sentence)
    
    asyncio.create_task(task())
    