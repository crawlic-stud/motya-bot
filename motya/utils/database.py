from typing import Any, List

import pymongo
from models import MessageData


class Database:
    def __init__(self, url: str, db_name: str) -> None:
        self.db = pymongo.MongoClient(url)[db_name]

    def _get_chat_collection(self, chat_id: int):
        return self.db[str(chat_id)]

    def _get_messages(self, chat_id: int) -> List[Any]:
        return self._get_chat_collection(chat_id).find()

    def save_messages(self, chat_id: int, messages: List[MessageData]) -> None:
        messages = [message.prepare_to_save() for message in messages]
        self._get_chat_collection(chat_id).insert_many(messages)

    def get_messages_from_chat(self, chat_id: int) -> List[str]:
        return [message["text"] for message in self._get_messages(chat_id)]

    def get_pastas(self) -> List[str]:
        return [pasta["text"] for pasta in self.db["pastas"].find()]
