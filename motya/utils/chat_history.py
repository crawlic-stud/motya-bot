from pathlib import Path
from typing import List
import json


CHAT_HISTORY_PATH = "chat_history"


def get_texts_from_json(path: Path) -> List[Path]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    messages = data.get("messages", [])
    texts = []
    for message in messages:
        message_text = message.get("text")
        if isinstance(message_text, str):
            texts.append(message_text)
        elif isinstance(message_text, list):
            texts.append(
                "".join(
                    [
                        item if isinstance(item, str) else item["text"]
                        for item in message_text
                    ]
                )
            )
    return texts


def save_texts_to_txt(path: Path, texts: List[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(texts))


def get_text_from_txt(path: Path) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# get_texts_from_json(Path.cwd() / "result.json")
