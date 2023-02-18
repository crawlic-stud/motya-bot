import os

from database import Database
from dotenv import load_dotenv


load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

messages_data = {}
db = Database(MONGO_URL, "motya")

