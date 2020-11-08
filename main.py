import duolingo
import argparse

from db import db_load, db_save
from game import play, load

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Duolingo word memorizer')
    parser.add_argument('-p', dest='password', type=str, help='Your duolingo password')
    parser.add_argument('-u', dest='username', type=str, help='Your duolingo username')
    parser.add_argument('--learning-lang', dest='learning_lang', type=str,
                        help='The language code for the language your are learning, e.g. dn for Dutch')
    parser.add_argument('--mother-lang', dest='mother_lang', type=str,
                        help='The language code for your mother tongue language, e.g en for english')
    parser.add_argument('--load', action='store_const', const=True,
                        help='Loads the newest vocabulary data for your user')
    parser.add_argument('--play', action='store_const', const=True, help='Start practicing')
    args = parser.parse_args()
    password = db_load('password')
    username = db_load('username')
    missing_pass = password is None and args.password is None
    missing_username = username is None and args.username is None
    if missing_pass or missing_username:
        print("Please log in with username and password")
        exit(1)
    if args.password is not None:
        db_save('password', args.password)
        password = args.password
    if args.username is not None:
        db_save('username', args.username)
        username = args.username

    learning_lang = db_load('learning_lang')
    mother_lang = db_load('mother_lang')
    if learning_lang is None and args.learning_lang is None:
        print("Please specify a learning language")
        exit(1)
    if args.learning_lang is not None:
        db_save('learning_lang', args.learning_lang)
        print(f"Set your learning language to {args.learning_lang}")
        learning_lang = args.learning_lang
    if mother_lang is None and args.mother_lang is None:
        print("Please specify your mother tongue language")
        exit(1)
    if args.mother_lang is not None:
        print(f"Set your mother tongue language to {args.mother_lang}")
        db_save('mother_lang', args.mother_lang)
        mother_lang = args.mother_lang

    lingo = None
    try:
        print(f"Logging you in as {username}...")
        lingo = duolingo.Duolingo(username, password)
        print(f"Successfully logged in!")
    except duolingo.DuolingoException:
        print('Failed to log you in. Check your username/password and try again.')
        exit(1)

    if args.load:
        load(lingo, learning_lang, mother_lang)
        exit()

    if args.play:
        play(lingo, learning_lang, mother_lang)
        exit()

    print("Specify an operation")
