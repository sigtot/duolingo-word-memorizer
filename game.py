from typing import List

import duolingo

from db import db_save, db_load

MAX_TRANSLATE_AMOUNT = 1000


def load(lingo: duolingo.Duolingo, learning_lang: str, mother_lang: str):
    vocab = lingo.get_vocabulary()
    words = vocab["vocab_overview"]
    print(f"Loaded vocabulary. You have studied {len(words)} words.")
    print(f"Loading translations to {mother_lang}...")
    translations = get_translations(lingo, words, learning_lang, mother_lang)
    print(translations)
    words = [{**word, "translations": translations[word["word_string"]]} for word in words]
    print(f"Loaded translations.")
    print(words)


def get_translations(lingo: duolingo.Duolingo, words: List[dict], learning_lang: str, mother_lang: str):
    word_strings = [word["word_string"] for word in words]
    translations = {}
    for start in range(0, len(word_strings), MAX_TRANSLATE_AMOUNT):
        end = start + MAX_TRANSLATE_AMOUNT
        translated_slice = lingo.get_translations(word_strings[start:end], source=learning_lang, target=mother_lang)
        translations.update(translated_slice)
        print(f"Loaded {end}/{len(word_strings)} translations.")
    return translations


def play(lingo: duolingo.Duolingo, learning_lang: str, mother_lang: str):
    print(f"Playing with learning language {learning_lang} and mother {mother_lang}")
    try:
        while True:
            sup = input("sup? ")
            print(f"You said {sup}")
    except KeyboardInterrupt:
        print("Bye for now")
