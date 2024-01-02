from aiogram import types
from aiogram.filters import Filter


class FileFilter(Filter):
    def __init__(self, extension: str) -> None:
        super().__init__()
        self.extension = extension

    async def __call__(self, message: types.Message) -> bool:
        if not message.document or not (message.document.file_name or "").endswith(
            self.extension
        ):
            return False
        return True
