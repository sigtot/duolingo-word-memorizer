import duolingo
import argparse

from db import db_load, db_save

lingo = duolingo.Duolingo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Duolingo word memorizer')
    parser.add_argument('-p', dest='password', type=str, help='Your duolingo password')
    parser.add_argument('-u', dest='username', type=str, help='Your duolingo username')
    args = parser.parse_args()
    print(f"Your gave me pass {args.password}")
    print(f"Your gave me username {args.username}")
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

    print(f"You are logged in as u: {username}, p: {password}")
