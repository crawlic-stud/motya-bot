from aiogram import types

from config import dp


@dp.message_handler()
async def save_message(message: types.Message):
    pass
