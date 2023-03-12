from typing import Union

from markovify import NewlineText


MAX_TRIES = 1000
MAX_WORDS = 150


def _catch_empty_chain(func):
    def wrapper(text: str):
        try:
            return func(text)
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


# def generate_random_answer(messages_list, keyword='hello!'):
#     # dumping all db data to string
#     text = f'{keyword}\n'
#     for message in messages_list:
#         text += message + '\n'

#     text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
#     answer_word = keyword.split(' ')
#     print(answer_word[0], keyword)
#     sentence = text_model.make_sentence_with_start(beginning=answer_word[0])

#     return sentence
