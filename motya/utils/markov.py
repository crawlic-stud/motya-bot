from functools import lru_cache
import logging
from typing import Union

from markovify import NewlineText


logger = logging.getLogger("markov")

MAX_TRIES = 1000
MAX_WORDS = 150


def _catch_empty_chain(func):
    def wrapper(text: str, *args, **kwargs):
        try:
            return func(text, *args, **kwargs)
        except KeyError:
            return ""

    return wrapper


@lru_cache
@_catch_empty_chain
def first_model(text: str) -> NewlineText:
    text_model = NewlineText(input_text=text, well_formed=False)
    return text_model


@_catch_empty_chain
def second_model(text: str) -> NewlineText:
    text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
    return text_model


@_catch_empty_chain
def first_try(text: str) -> Union[str, None]:
    text_model = first_model(text)
    sentence = text_model.make_sentence(max_words=MAX_WORDS)
    return sentence


@_catch_empty_chain
def second_try(text: str) -> Union[str, None]:
    text_model = first_model(text)
    sentence = text_model.make_sentence(tries=MAX_TRIES, max_words=MAX_WORDS)
    return sentence


@_catch_empty_chain
def third_try(text: str) -> Union[str, None]:
    text_model = second_model(text)
    sentence = text_model.make_sentence(tries=MAX_TRIES)
    return sentence


@_catch_empty_chain
def generate_sentence(text: str) -> str:
    sentence = first_try(text)
    n_try = 1
    if not sentence:
        sentence = second_try(text)
        n_try = 2
    if not sentence:
        sentence = third_try(text) or ""
        n_try = 3
    logger.info(f"tries: {n_try}")
    return sentence


@_catch_empty_chain
def generate_sentence_with_start(text, keyword):
    text_model = NewlineText(input_text=text, well_formed=False)
    sentence = text_model.make_sentence_with_start(
        beginning=keyword, strict=False, tries=MAX_TRIES
    )
    return sentence or ""
