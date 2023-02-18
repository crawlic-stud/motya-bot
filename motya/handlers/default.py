from aiogram import types

from config import dp


@dp.message_handler()
async def send_start(message: types.Message):
    pass
