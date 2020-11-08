from typing import List

import duolingo


def load(lingo: duolingo.Duolingo):
    vocab = lingo.get_vocabulary()
    words = get_words(vocab)
    print(words)


def get_words(vocab: dict) -> List[str]:
    vocab_overview = vocab['vocab_overview']
    return [word_data['word_string'] for word_data in vocab_overview]


def play(lingo: duolingo.Duolingo, learning_lang: str, mother_lang: str):
    print(f"Playing with learning language {learning_lang} and mother {mother_lang}")
    try:
        while True:
            sup = input("sup? ")
            print(f"You said {sup}")
    except KeyboardInterrupt:
        print("Bye for now")
