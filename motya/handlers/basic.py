from aiogram import types
from config import dp


@dp.message_handler(commands=["start"])
async def send_start(message: types.Message):
    await message.answer("Привет!")
