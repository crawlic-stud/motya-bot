import firebase_admin as fba
from firebase_admin import firestore

from dataclasses import dataclass, asdict


@dataclass
class MessageData:
    user_id: int
    text: str


class Database:
    def __init__(self, database_url, key_path):
        cred = fba.credentials.Certificate(key_path)
        fba.initialize_app(cred, {'databaseURL': database_url})
        self.client = firestore.client()

    def _get_chat_collection(self, chat_id: int):
        return self.client.collection(str(chat_id))
    
    def _get_messages(self, chat_id: int):
        messages = (
            document.to_dict() for document in self._get_chat_collection(chat_id).get()
        )
        return messages
    
    def add_message(self, user_id: int, chat_id: int, message: str):
        collection = self._get_chat_collection(chat_id)
        collection.add(
            asdict(
                MessageData(user_id=user_id, text=message)
            )
        )
    
    def get_messages_from_chat(self, chat_id: int):
        return [message["text"] for message in self._get_messages(chat_id)]
        