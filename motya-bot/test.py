from config import db 
from database import firestore


# db.add_message("test", "Очень длинное сообщение " * 100)
chat_id = 12345
user_id = 0
message = "test"
db.add_message(user_id, chat_id, message)
messages = db._get_messages(12345)
messages = db.get_messages_from_chat(12346)
messages = db.get_messages_from_chat(12345)
print(messages)
