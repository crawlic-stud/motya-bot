from markovify import NewlineText, Text

from data.anekdots import combine_all_anekdots


if __name__ == "__main__":
    path = combine_all_anekdots()
    text = path.read_text(encoding="utf-8")
    model = NewlineText(text, well_formed=False)
    for _ in range(25):
        print(model.make_sentence())
        print("-" * 50)
