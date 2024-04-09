from markovify import NewlineText

from data.anekdots import combine_all_anekdots

from utils.wordcloud_generate import create_wordcloud

from config import common_db


def test_anekdots():
    path = combine_all_anekdots()
    text = path.read_text(encoding="utf-8")
    model = NewlineText(text, well_formed=False)
    for _ in range(25):
        print(model.make_sentence())
        print("-" * 50)


def test_wordcloud():
    create_wordcloud(-645455290, common_db, min_word_length=1)


if __name__ == "__main__":
    test_wordcloud()
