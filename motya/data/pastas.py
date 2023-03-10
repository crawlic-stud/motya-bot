import time
import requests
from bs4 import BeautifulSoup

from config import db, motya
from models import MessageData


def feed_copypastas_to_bot():
    pastas_collection = "pastas"
    pastas = []
    
    def save_pastas():
        print("\n---------------------SAVING---------------------\n")
        db.db[pastas_collection].insert_many(
            [MessageData(0, text).prepare_to_save() for text in pastas if text] 
        )
    
    for i in range(500, 1500):
        try:
            req = requests.get(f"https://copypastas.ru/copypasta/{i}/")
            soup = BeautifulSoup(req.text, "html.parser")
            element = soup.find("h2", string="Текст копипасты")
            parent = element.parent
            pasta = parent.select("div > div")[0].text
            print(pasta)
            print("-" * 50)
            pastas += list(map(str.strip, pasta.split(".")))
            time.sleep(0.1)
            
            if len(pastas) >= 100:
                save_pastas()
                pastas = []
                
        except Exception as e:
            print(e)
            continue
    
    save_pastas()