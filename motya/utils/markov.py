import random

from markovify import NewlineText, Text


# TODO: refactor those functions
def generate_random_sentence(messages):
    if not messages:
        return

    random.shuffle(messages) 
    text = ". ".join(messages)
    text_model = Text(input_text=text, well_formed=True, state_size=1)
    # text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000)
    return sentence.lower()


def generate_random_answer(messages_list, keyword='������ ���'):
    # dumping all db data to string
    text = f'{keyword}\n'
    for message in messages_list:
        text += message + '\n'

    text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
    answer_word = keyword.split(' ')
    print(answer_word[0], keyword)
    sentence = text_model.make_sentence_with_start(beginning=answer_word[0])

    return sentence