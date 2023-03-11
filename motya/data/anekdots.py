from typing import Dict
from pathlib import Path
import time
import os

import requests
from bs4 import BeautifulSoup


ANEKDOTS_FOLDER = Path.cwd() / "motya" / "files" / "anekdots" 



def get_tags_links() -> Dict[str, str]:
    base_url = "https://www.anekdot.ru"
    req = requests.get(base_url + "/tags/")
    if not req.status_code == 200:
        return {}
    soup = BeautifulSoup(req.text, "html.parser")
    tags_cloud = soup.select_one(".tags-cloud")
    tags = tags_cloud.find_all("a")
    result = {}
    for tag in tags:
        result[tag.text] = base_url + tag["href"]
    return result


def get_page_text(base_url: str, page_number: int) -> str:
    req = requests.get(f"{base_url}/{page_number}")
    if not req.status_code == 200:
        return ""
    for response in req.history:
        if response.status_code == 302:
            return ""
    return req.text     


def save_all_anekdots() -> None:
    if not ANEKDOTS_FOLDER.exists():
        os.makedirs(ANEKDOTS_FOLDER)
    tags_links = get_tags_links()
    for tag_name, tag_url in tags_links.items():
        page = 1
        anekdots_by_tag = []
        html = get_page_text(tag_url, page) 
        
        if list(ANEKDOTS_FOLDER.glob(f"{tag_name}*")):
            print("Already exist:", tag_name)
            continue
        
        while html:
            print(f"Parsing {tag_name=}, {page=}")
            html = get_page_text(tag_url, page)
            soup = BeautifulSoup(html, "html.parser")
            
            elements = soup.select(".topicbox .text")
            anekdots_this_page = [elem.text for elem in elements]
            anekdots_by_tag += anekdots_this_page
            page += 1
            time.sleep(0.05)
        
        print("-"*50)    
        path = ANEKDOTS_FOLDER / f"{tag_name}.txt"
        path.write_text("\n".join(anekdots_by_tag), encoding="utf-8")
        print(f"Saved anekdots with {tag_name=}, last_page={page}")    
        print("-"*50)    



def combine_all_anekdots() -> None:
    all_path = ANEKDOTS_FOLDER / "anekdots.txt"
    all_path.write_text("")
    with open(all_path, "a", encoding="utf-8") as f:
        for path in ANEKDOTS_FOLDER.glob("*.txt"):
            f.write(path.read_text(encoding="utf-8") + "\n")
    

# print(get_tags_links())
# save_all_anekdots()
combine_all_anekdots()
