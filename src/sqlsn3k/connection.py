import os
import sqlite3


def connect(path):
    """
    Attempts to connect to the given database
    """
    try:
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        print(f'Error opening database "{path}":\n{e}')
        return None


def connection_dialogue(path):
    """
    Handles connecting to a database. Prompts the user to ask if they are sure
    that they want to create a new database if the requested database does not
    exist or is otherwise not found.
    """
    if type(path) is list:
        path = ''.join(path).strip()
    elif type(path) is not str:
        path = str(path)
    if os.path.isfile(path):
        return connect(path)
    else:
        yn = input(f'Database "{path}" does not exist,'
                   + " would you like to create it? (y/n):")
        if yn.lower() == 'y':
            return connect(path)
        else:
            return None
