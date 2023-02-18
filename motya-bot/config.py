import os
import logging

from aiogram import Bot, Dispatcher

from utils.database import Database
from dotenv import load_dotenv


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
PROD_TOKEN = os.getenv("TG_TOKEN")
TEST_TOKEN = os.getenv("TG_TEST_TOKEN")

TG_TOKEN = TEST_TOKEN

logging.basicConfig(level=logging.INFO)

motya = Bot(TG_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=motya)

messages_data = {}
db = Database(MONGO_URL, "motya")
