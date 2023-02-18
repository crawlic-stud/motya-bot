import time
import asyncio

from config import db, motya
from models import MessageData


if __name__ == "__main__":
    # print(db.save_messages(123456, [MessageData(1, "text") for _ in range(3)]))
    # print(db._get_messages(123456))
    print(db.get_messages_from_chat(-1001669933530))
    # asyncio.run(motya.send_message(-1001669933530, "test"))
    ...