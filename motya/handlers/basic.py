from aiogram import types, Router
from aiogram.filters.command import CommandStart


router = Router(name="basic")


@router.message(CommandStart())
async def send_start(message: types.Message):
    await message.answer(
        "привет, я мотя! добавляй меня в чатик и я разбавлю ваши серые будни!"
    )
