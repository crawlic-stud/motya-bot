from typing import List

import pymongo

from models import MessageData


class Database:
    def __init__(self, url: str, db_name: str):    
        self.client = pymongo.MongoClient(url)[db_name]

    def _get_chat_collection(self, chat_id: int):
        return self.client[str(chat_id)]
    
    def _get_messages(self, chat_id: int):
        return self._get_chat_collection(chat_id).find()
    
    def add_messages(self, chat_id: int, messages: List[MessageData]):
        ...
                
    def get_messages_from_chat(self, chat_id: int):
        return [message["text"] for message in self._get_messages(chat_id)]
    