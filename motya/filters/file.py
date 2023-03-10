from aiogram.dispatcher.filters import Filter
from aiogram import types


class FileFilter(Filter):
    def __init__(
        self, 
        extension: str 
     ) -> None:
        super().__init__()
        self.extension = extension
        
    async def check(self, message: types.Message) -> bool:
        if not message.document or not message.document.file_name.endswith(self.extension):
            return False
        return True
