from config import messages_data
from models import MessageData


class MessageManager:
    def __init__(self, chat_id: int) -> None:
        if not messages_data.get(chat_id):
            messages_data[chat_id] = []
        self.data = messages_data[chat_id]
        
    def add(self, message: MessageData):
        self.data.append(message)
    
    def clear(self):
        self.data = []
