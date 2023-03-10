import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from utils.database import Database
from middlewares.message_saver import MessageSaver
from middlewares.random_sender import RandomSender


load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
PROD_TOKEN = os.getenv("TG_TOKEN")
TEST_TOKEN = os.getenv("TG_TEST_TOKEN")

TG_TOKEN = TEST_TOKEN

logging.basicConfig(level=logging.INFO)

motya = Bot(TG_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=motya)

# dict to temporary store messages 
messages_data = {}
chat_offset = {}
db = Database(MONGO_URL, "motya")

# middleware for saving messages to DB
dp.setup_middleware(MessageSaver(messages_data, db))
dp.setup_middleware(RandomSender(db))

