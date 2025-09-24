from datetime import datetime
from functools import wraps
import logging
import sys
from typing import Any

import pymongo
from pymongo.cursor import Cursor

from models import MessageData, ArgumentTimeElapsed


rating_cache = set()
logger = logging.getLogger("db")

MESSAGES_LIMIT = 15_000
MAX_CACHE_SIZE_KB = 50 * 1024  # 50 MB
CACHE_MESSAGES_SECONDS = 300  # 5 minutes


class ExpiringCache:
    def __init__(self, expiration_time):
        self.expiration_time = expiration_time
        self.cache = {}

    def cache_size_kb(self):
        total_size = sys.getsizeof(self.cache)
        for key, value in self.cache.items():
            total_size += sys.getsizeof(key) + sys.getsizeof(value)
        return total_size / 1024

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args):
            cache_size = self.cache_size_kb()
            logger.info(f"Cache size {cache_size} KB")
            if cache_size > MAX_CACHE_SIZE_KB:
                self.cache.clear()
            current_time = datetime.now().timestamp()
            if args in self.cache:
                value, timestamp = self.cache[args]
                if current_time - timestamp < self.expiration_time:
                    return value
            logger.info(f"Cache miss for {func.__name__} with args {args}")
            value = func(*args)
            self.cache[args] = (value, current_time)
            return value

        return wrapper


class CommonDb:
    def __init__(self, url: str, db_name: str) -> None:
        self.db = pymongo.MongoClient(url)[db_name]

    def _get_chat_collection(self, chat_id: int):
        return self.db[str(chat_id)]

    def _get_messages(self, chat_id: int, limit: int = 0) -> Cursor[Any]:
        logger.info(f"Getting messages from chat {chat_id} with limit {limit}")
        if not limit:
            limit = MESSAGES_LIMIT
        return self._get_chat_collection(chat_id).find().limit(limit).sort("_id", pymongo.DESCENDING)

    def save_messages(self, chat_id: int, messages: list[MessageData]) -> None:
        new_messages = [message.prepare_to_save() for message in messages]
        self._get_chat_collection(chat_id).insert_many(new_messages)

    @ExpiringCache(expiration_time=CACHE_MESSAGES_SECONDS)
    def get_messages_from_chat(self, chat_id: int, limit: int = 0) -> list[str]:
        messages = [message["text"] for message in self._get_messages(chat_id, limit)]
        logger.info(f"Got {len(messages)} messages from chat {chat_id}")
        return messages

    @ExpiringCache(expiration_time=10)
    def get_messages_for_ai(self, chat_id: int, limit: int = 0) -> list[str]:
        messages = [f"{message['user_id']}:\n{message['text']}" for message in self._get_messages(chat_id, limit)]
        logger.info(f"Got {len(messages)} messages from chat for ai {chat_id}")
        return messages


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
