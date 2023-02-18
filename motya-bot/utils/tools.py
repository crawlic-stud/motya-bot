

def words_after(message, word):
    words = message.split(' ')
    word_index = words.index(word) + 1
    text = ''
    return " ".join(words[word_index:])
