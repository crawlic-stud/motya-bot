import time

import requests
from bs4 import BeautifulSoup

from config import pastas_db
from models import MessageData


def save_pastas(pastas):
    print("\n---------------------SAVING---------------------\n")
    pastas_db.insert_pastas(
        [MessageData(0, text).prepare_to_save() for text in pastas if text]
    )


def feed_copypastas_to_bot():
    pastas = []
    for i in range(500, 1500):
        try:
            req = requests.get(f"https://copypastas.ru/copypasta/{i}/")
            soup = BeautifulSoup(req.text, "html.parser")
            element = soup.find("h2", string="Текст копипасты")  # type: ignore
            parent = element.parent  # type: ignore
            pasta = parent.select("div > div")[0].text  # type: ignore
            print(pasta)
            print("-" * 50)
            pastas += list(map(str.strip, pasta.split(".")))
            time.sleep(0.1)

            if len(pastas) >= 100:
                save_pastas(pastas)
                pastas = []

        except Exception as e:
            print(e)
            continue

    save_pastas(pastas)
