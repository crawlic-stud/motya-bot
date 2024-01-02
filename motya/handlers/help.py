from aiogram import types, Router
from aiogram.filters.command import Command

from filters.motya_command import motya_commands, MotyaCommand


router = Router(name="help")


@router.message(Command("help"))
@router.message(MotyaCommand(["что умеешь"], strict=True))
async def send_help(message: types.Message):
    await message.answer("привет, я мотя! воть что я умею:")
    help_text = "\n".join([command.render_html() for command in motya_commands])
    await message.answer(help_text)
