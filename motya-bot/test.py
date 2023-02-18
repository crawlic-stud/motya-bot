import time
import asyncio

from config import db, motya
from models import MessageData
from utils.markov import generate_random_sentence


if __name__ == "__main__":
    # print(db.save_messages(123456, [MessageData(1, "text") for _ in range(3)]))
    # print(db._get_messages(123456))
    messages = db.get_messages_from_chat(-1001669933530)
    print(generate_random_sentence(messages))
    # asyncio.run(motya.send_message(-1001669933530, "test"))
    ...
    