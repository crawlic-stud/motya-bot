from wordcloud import WordCloud

from .database import CommonDb


def create_wordcloud(chat_id: int, db: CommonDb, min_word_length: int = 5):
    messages = db.get_messages_from_chat(chat_id)
    messages = [
        [word for word in message.split() if len(word) >= min_word_length]
        for message in messages
    ]
    new_messages = []
    for message in messages:
        new_messages.extend(message)
    print(len(new_messages))
    text = " ".join(new_messages)
    wordcloud = WordCloud(width=1920, height=1080, background_color="white").generate(
        text
    )

    img = wordcloud.to_image()
    img.show()
    # plt.figure(figsize=(10, 5))
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
