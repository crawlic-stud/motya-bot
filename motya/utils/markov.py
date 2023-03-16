from typing import Union

from markovify import NewlineText


MAX_TRIES = 1000
MAX_WORDS = 150


def _catch_empty_chain(func):
    def wrapper(text: str, *args, **kwargs):
        try:
            return func(text, *args, **kwargs)
        except KeyError:
            return ""
    return wrapper


@_catch_empty_chain
def first_try(text: str) -> Union[str, None]:
    text_model = NewlineText(input_text=text, well_formed=False)
    sentence = text_model.make_sentence(max_words=MAX_WORDS)
    return sentence


@_catch_empty_chain
def second_try(text: str) -> Union[str, None]:
    text_model = NewlineText(input_text=text, well_formed=False)
    sentence = text_model.make_sentence(tries=MAX_TRIES, max_words=MAX_WORDS)
    return sentence


@_catch_empty_chain
def third_try(text: str) -> Union[str, None]:
    text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=MAX_TRIES)
    return sentence


@_catch_empty_chain
def generate_sentence(text: str) -> str:
    sentence = first_try(text)
    if not sentence:
        sentence = second_try(text)
    if not sentence:
        sentence = third_try(text) or ""
    return sentence


@_catch_empty_chain
def generate_sentence_with_start(text, keyword):
    text_model = NewlineText(input_text=text, well_formed=False)
    sentence = text_model.make_sentence_with_start(
        beginning=keyword,
        strict=False,
        tries=MAX_TRIES)
    return sentence or ""
