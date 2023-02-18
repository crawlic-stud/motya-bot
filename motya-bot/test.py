import time

from config import db 


print(list(db._get_chat_collection(123456).find()))
print(db._get_messages(123456))
print(db.get_messages_from_chat(123456))

