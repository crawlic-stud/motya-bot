from datetime import datetime
from functools import lru_cache
from typing import Any

import pymongo
from models import MessageData, ArgumentTimeElapsed


rating_cache = set()


class CommonDb:
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


class Database(CommonDb):
    def __init__(self, url: str, db_name: str, collection_name: str) -> None:
        super().__init__(url, db_name)
        self.collection = self.db[collection_name]


class PastasDb(Database):
    def get_pastas(self) -> list[str]:
        return [pasta["text"] for pasta in self.collection.find()]

    def insert_pastas(self, pastas: list[dict[str, Any]]):
        self.collection.insert_many(pastas)


class ArgumentsDb(Database):
    def get_days_since_last_argument(self, chat_id: int) -> ArgumentTimeElapsed:
        arg_obj = self.collection.find_one({"chat_id": chat_id}, {"date": 1}) or {}
        date: datetime = arg_obj.get("date", datetime.now())
        delta = datetime.now() - date
        return ArgumentTimeElapsed.from_timedelta(delta)

    def insert_new_argument(self, chat_id: int) -> None:
        self.collection.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "chat_id": chat_id,
                    "date": datetime.now(),
                }
            },
            upsert=True,
        )


class SongsDb(Database):
    def get_songs(self, artist: str) -> list[str]:
        return [song["lyrics"] for song in self.collection.find({"artist": artist})]

    def add_songs(self, artist: str, songs_lyrics: list[str]) -> None:
        songs_objs = [{"artist": artist, "lyrics": song} for song in songs_lyrics]
        self.collection.insert_many(songs_objs)

    def get_all_songs(self):
        return [song["lyrics"] for song in self.collection.find()]


class RatingDb(Database):
    def is_rated(self, message_id: str) -> bool:
        if message_id in rating_cache:
            return True
        res = self.collection.find_one({"message_id": message_id}) is not None
        if res:
            rating_cache.add(message_id)
        return res

    def add_to_rating(self, message_id: str):
        self.collection.insert_one({"message_id": message_id})
