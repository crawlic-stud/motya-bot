import os
from pathlib import Path

from aiogram import types, F, Router

from config import motya
from filters.file import FileFilter
from utils.chat_history import CHAT_HISTORY_PATH, get_texts_from_json, save_texts_to_txt


router = Router(name="json_file")


@router.message(FileFilter(".json"), F.document)
async def handle_json(message: types.Message):
    try:
        path = Path(CHAT_HISTORY_PATH) / f"{message.chat.id}.json"
        file_id = message.document.file_id if message.document else ""
        await motya.download(file_id, destination=path)
        texts = get_texts_from_json(path)
        os.remove(path)
        save_texts_to_txt(Path(CHAT_HISTORY_PATH) / f"{message.chat.id}.txt", texts)
        await message.reply("сохранил историю вашего чатика :з")
    except Exception as e:
        print(e)
        await message.reply("я не могу кушать файлы больше 20мб :(")
