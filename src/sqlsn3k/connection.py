import os
import sqlite3

from sqlite_helpers import modifies_db
from string_manip import to_string
from table import Table


class SQLConnection:
    def __init__(self, path):
        if type(path) is list:
            self.path = ''.join(path).strip()
        elif type(path) is str:
            self.path = path
        else:
            self.path = str(path)
        self.db_name = self.path.split('/')[-1]
        self.connection = self.connection_dialogue()
        self.modified = False

    def connect(self):
        """
        Attempts to connect to the given database
        """
        try:
            connection = sqlite3.connect(self.path)
            connection.row_factory = sqlite3.Row
            return connection
        except Exception as e:
            print(f'Error opening database "{self.path}":\n{e}')
            return None

    def connection_dialogue(self):
        """
        Handles connecting to a database. Prompts the user to ask if they are
        sure that they want to create a new database if the requested database
        does not exist or is otherwise not found.
        """
        if os.path.isfile(self.path):
            return self.connect()
        else:
            yn = input(f'Database "{self.path}" does not exist,'
                       + " would you like to create it? (y/n):")
            if yn.lower() == 'y':
                return self.connect()
            else:
                return None

    def execute(self, query):
        """
        Executes the SQLite query and returns the result; iff it fails, returns
        a str with the exception
        """
        query = to_string(query, list_delimiter=' ')
        cursor = self.connection.cursor()
        try:
            result = Table(cursor.execute(query))
            if modifies_db(query):
                self.modified = True
            try:
                return to_string(result)
            except Exception as e:
                return f'connection:exectue:execution: {e}'
        except ValueError as ve:
            return f'connection:exectue: {ve}\nquery was: {type(query)}'
        except Exception as e:
            return f'connection:execute: {e}'

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
