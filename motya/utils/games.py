from pathlib import Path
import random
from dataclasses import dataclass, field

from config import db

PICS = (Path.cwd() / "motya/sprites.txt").read_text().split(";")


@dataclass
class HangmanGame:
    word: str
    step: int = 0
    guessed_letters: set[str] = field(default_factory=set)
    wrong_letters: set[str] = field(default_factory=set)

    @property
    def lost(self):
        return self.step == len(PICS) - 1

    @property
    def won(self):
        return all(letter in self.guessed_letters for letter in self.word)

    def render(self):
        word = self.word
        for letter in self.word.strip():
            if letter in self.guessed_letters:
                continue
            word = word.replace(letter, "_ ")
        if not self.lost:
            return f"{word}\n\n{PICS[self.step]}"
        return f"{self.word}\n\n{PICS[-1]}"


@dataclass
class WordleGame:
    word: str
    prev_guesses: list[str] = field(default_factory=list)

    @property
    def lost(self):
        return len(self.prev_guesses) >= len(self.word)

    def calculate_colors(self, guess: str) -> str:
        colors = ""
        for original_letter, guessed_letter in zip(self.word, guess):
            if original_letter == guessed_letter:
                colors += "🟩"
            elif guessed_letter in self.word:
                colors += "🟨"
            else:
                colors += "⬜️"
        return colors

    def render(self) -> str:
        game_rendered = []
        for prev_guess in self.prev_guesses:
            game_rendered.append(self.calculate_colors(prev_guess))
            game_rendered.append("   ".join(prev_guess).upper())
        return "\n".join(game_rendered)


def messages_to_words(messages: list[str], max_word_length: int = 10, min_word_length: int = 5) -> list[str]:
    words = []
    for message in messages:
        msg_words = message.split()
        msg_words = [word for word in msg_words if len(
            word) <= max_word_length and len(word) > min_word_length and word.isalpha()]
        words.extend(msg_words)
    return words


def get_word(chat_id: int, max_length: int):
    all_messages = db.get_messages_from_chat(chat_id)
    words = messages_to_words(all_messages, max_length) or ["писька"]
    word = random.choice(words)
    return word


if __name__ == "__main__":
    print(PICS)
