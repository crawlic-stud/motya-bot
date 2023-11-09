import os
from pathlib import Path

from aiogram import types
from aiogram.utils.exceptions import FileIsTooBig
from config import dp
from filters.file import FileFilter
from utils.chat_history import CHAT_HISTORY_PATH, get_texts_from_json, save_texts_to_txt


@dp.message_handler(FileFilter(".json"), content_types=[types.ContentType.DOCUMENT])
async def handle_json(message: types.Message):
    try:
        path = Path(CHAT_HISTORY_PATH) / f"{message.chat.id}.json"
        await message.document.download(destination_file=path)
        texts = get_texts_from_json(path)
        os.remove(path)
        save_texts_to_txt(Path(CHAT_HISTORY_PATH) / f"{message.chat.id}.txt", texts)
        await message.reply("сохранил историю вашего чатика :з")
    except FileIsTooBig:
        await message.reply("я не могу кушать файлы больше 20мб :(")
