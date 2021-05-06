import os
import sqlite3

from sqlite_helpers import modifies_db
from string_manip import to_string


class SQLConnection:
    def __init__(self, path):
        path = str(path)
        self.path = path
        self.db_name = path.split('/')[-1]
        self.connection = self.connection_dialogue(path)
        self.modified = False

    def connect(self, path):
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

    def connection_dialogue(self, path):
        """
        Handles connecting to a database. Prompts the user to ask if they are
        sure that they want to create a new database if the requested database
        does not exist or is otherwise not found.
        """
        if type(path) is list:
            path = ''.join(path).strip()
        elif type(path) is not str:
            path = str(path)
        if os.path.isfile(path):
            return self.connect(path)
        else:
            yn = input(f'Database "{path}" does not exist,'
                       + " would you like to create it? (y/n):")
            if yn.lower() == 'y':
                return self.connect(path)
            else:
                return None

    def execute(self, query):
        """
        Executes the SQLite query and returns the result; iff it fails, returns
        a str with the exception
        """
        cursor = self.connection.cursor()
        try:
            result = cursor.execute(query)
            if modifies_db(query):
                self.modified = True
            try:
                return to_string(result)
            except Exception as e:
                return f'connection:exectue:execution: {e}'
        except Exception as e:
            return f'connection:exectue: {e}'

    def close(self, commit='n', failed=False):
        """
        Attemps to close the SQL connection
        """
        if self.connection is not None:
            if self.modified and not failed:
                if commit.lower() == 'y':
                    print("Commiting and closing the database...")
                    self.connection.commit()
            self.connection.close()
