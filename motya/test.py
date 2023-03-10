import time
import requests
from bs4 import BeautifulSoup

from config import db, motya
from models import MessageData


def feed_copypastas_to_bot():
    test_chat = -1001669933530
    pastas = []
    
    def save_pastas():
        print("\n---------------------SAVING---------------------\n")
        db.save_messages(
            test_chat,
            [MessageData(0, text) for text in pastas if text] 
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
    

if __name__ == "__main__":
    # print(db.save_messages(123456, [MessageData(1, "text") for _ in range(3)]))
    # print(db._get_messages(123456))
    # messages = db.get_messages_from_chat(-1001669933530)
    # print(generate_random_sentence(messages))
    # asyncio.run(motya.send_message(-1001669933530, "test"))
    feed_copypastas_to_bot()
    ...
    