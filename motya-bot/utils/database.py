from typing import List

import pymongo

from models import MessageData


class Database:
    def __init__(self, url: str, db_name: str):    
        self.db = pymongo.MongoClient(url)[db_name]

    def _get_chat_collection(self, chat_id: int):
        return self.db[str(chat_id)]
    
    def _get_messages(self, chat_id: int):
        return self._get_chat_collection(chat_id).find()
    
    def save_messages(self, chat_id: int, messages: List[MessageData]):
        messages = [message.prepare_to_save() for message in messages]
        self._get_chat_collection(chat_id).insert_many(messages)
                
    def get_messages_from_chat(self, chat_id: int):
        return [message["text"] for message in self._get_messages(chat_id)]
    