import random


def words_after(message: str, word: str) -> str:
    words = message.split(' ')
    word_index = words.index(word) + 1
    return " ".join(words[word_index:])


def roll_chance(probability: float) -> bool:
    return not random.randint(0, int(1 / probability))
