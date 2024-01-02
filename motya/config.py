import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from middlewares.message_saver import MessageSaver
from middlewares.random_sender import RandomSender
from utils.database import ArgumentsDb, CommonDb, PastasDb, SongsDb
from utils.image_api import Text2ImageAPI

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
PROD_TOKEN = os.getenv("TG_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # type: ignore

TG_TOKEN = PROD_TOKEN

logging.basicConfig(level=logging.INFO)

motya = Bot(TG_TOKEN, parse_mode="HTML")  # type: ignore
dp = Dispatcher(bot=motya, storage=MemoryStorage())

# dict to temporary store messages
messages_data = {}
chat_offset = {}

# image API
API_KEY = os.getenv("FUSION_API_KEY")
SECRET_KEY = os.getenv("FUSION_SECRET_KEY")
image_api = Text2ImageAPI("https://api-key.fusionbrain.ai/", API_KEY, SECRET_KEY)

DB_NAME = "motya"
common_db = CommonDb(MONGO_URL, DB_NAME)  # type: ignore
pastas_db = PastasDb(MONGO_URL, DB_NAME, "pastas")  # type: ignore
arguments_db = ArgumentsDb(MONGO_URL, DB_NAME, "arguments")  # type: ignore
songs_db = SongsDb(MONGO_URL, DB_NAME, "songs")  # type: ignore


# middleware for saving messages to DB
dp.message.middleware(MessageSaver(messages_data, common_db))
dp.message.middleware(RandomSender(common_db, motya))
