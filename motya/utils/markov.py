from markovify import NewlineText


def generate_random_sentence(messages_list):
    # dumping all db data to string
    text = ''
    for message in messages_list:
        text += message + '\n'

    # print(text)
    text_model = NewlineText(input_text=text, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000)

    return sentence


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