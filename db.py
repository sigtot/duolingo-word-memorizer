import shelve

SHELVE_FILE = 'shelve.p'


def db_load(key: str):
    with shelve.open(SHELVE_FILE) as shelf:
        return shelf.get(key)


def db_save(key: str, data):
    with shelve.open(SHELVE_FILE) as shelf:
        shelf[key] = data
