from datetime import datetime
from typing import Any

import pymongo
from models import MessageData, ArgumentTimeElapsed


class Database:
    def __init__(self, url: str, db_name: str) -> None:
        self.db = pymongo.MongoClient(url)[db_name]

    def _get_chat_collection(self, chat_id: int):
        return self.db[str(chat_id)]

    def _get_messages(self, chat_id: int) -> list[Any]:
        return [item for item in self._get_chat_collection(chat_id).find()]

    def save_messages(self, chat_id: int, messages: list[MessageData]) -> None:
        new_messages = [message.prepare_to_save() for message in messages]
        self._get_chat_collection(chat_id).insert_many(new_messages)

    def get_messages_from_chat(self, chat_id: int) -> list[str]:
        return [message["text"] for message in self._get_messages(chat_id)]

    def get_pastas(self) -> list[str]:
        return [pasta["text"] for pasta in self.db["pastas"].find()]

    def get_days_since_last_argument(self, chat_id: int) -> ArgumentTimeElapsed:
        collection = self.db["arguments"]
        arg_obj = collection.find_one({"chat_id": chat_id}, {"date": 1}) or {}
        date: datetime = arg_obj.get("date", datetime.now())
        delta = datetime.now() - date
        return ArgumentTimeElapsed.from_timedelta(delta)

    def insert_new_argument(self, chat_id: int) -> None:
        collection = self.db["arguments"]
        collection.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "chat_id": chat_id,
                    "date": datetime.now(),
                }
            },
            upsert=True,
        )
