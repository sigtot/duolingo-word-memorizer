import random
from typing import List

import duolingo

from db import db_save, db_load

MAX_TRANSLATE_AMOUNT = 1000


def load(lingo: duolingo.Duolingo, learning_lang: str, mother_lang: str):
    vocab = lingo.get_vocabulary()
    old_words = db_load("words") or []
    words = vocab["vocab_overview"]
    print(f"Loaded vocabulary. You have studied {len(words)} words ({len(words) - len(old_words)} new since last time).")
    print(f"Loading translations to {mother_lang}...")
    translations = get_translations(lingo, words, learning_lang, mother_lang)
    words = [{**word, "translations": translations[word["word_string"]]} for word in words]
    print(f"Loaded translations.")
    updated_words = init_practice_counts(update_word_dict(old_words, words))
    db_save("words", updated_words)
    print("Updated")


def update_word_dict(old_words: List[dict], new_words: List[dict]) -> List[dict]:
    combined_words = []
    for new_word in new_words:
        try:
            old_word = find_word(new_word, old_words)
            combined_words.append({**old_word, **new_word})
        except StopIteration:
            combined_words.append(new_word)
    return combined_words


# Raises `StopIteration` if no word is found
def find_word(word: dict, words: List[dict]) -> dict:
    return next(w for w in words if w["word_string"] == word["word_string"])


def init_practice_counts(words: List[dict]) -> List[dict]:
    return [{**word, "practice_count": word.get("practice_count") or 0} for word in words]


def get_translations(lingo: duolingo.Duolingo, words: List[dict], learning_lang: str, mother_lang: str):
    word_strings = [word["word_string"] for word in words]
    translations = {}
    for start in range(0, len(word_strings), MAX_TRANSLATE_AMOUNT):
        end = start + MAX_TRANSLATE_AMOUNT
        translated_slice = lingo.get_translations(word_strings[start:end], source=learning_lang, target=mother_lang)
        translations.update(translated_slice)
        print(f"Loaded {end}/{len(word_strings)} translations.")
    return translations


# Assumes word exists in db and that
def inc_practice_count(word: dict):
    words = db_load("words")
    old_word = find_word(word, words)
    old_word["practice_count"] += 1
    db_save("words", words)


def play(learning_lang: str, mother_lang: str):
    print(f"Playing with learning language {learning_lang} and mother {mother_lang}")
    words = db_load("words")
    correct_words = []
    failed_words = []
    try:
        while True:
            word = random.choice(words)
            word_string = word["word_string"]
            translations = word["translations"]
            user_translation = input(f"{word_string}: ")
            if user_translation in translations:
                print("CORRECT")
                inc_practice_count(word)
                correct_words.append(word)
            else:
                print(f"WRONG: Correct translations: {translations}.")
                failed_words.append(word)
                _ = input("Hit enter for next word.")
    except KeyboardInterrupt:
        print(f"Practiced {len(correct_words) + len(failed_words)} ({len(correct_words)} correct)")
        print("Bye for now")
