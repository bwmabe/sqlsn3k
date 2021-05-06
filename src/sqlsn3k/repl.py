import readline
import os

from connection import connection_dialogue
from sqlite_helpers import modifies_db
from string_manip import to_string


class REPL:
    histfile = os.path.join(os.path.expanduser("~"), ".sqlsn3k_history")

    def __init__(self, db_name=None, database_connection=None):
        """
        Initializes the REPL object. Also initializes the readline library's
        'history' functionality.
        db_name and database_connection are optional arguments in case a
        database connection is establish when launching the program from the
        command line.
        """
        self.connection = database_connection
        self.db_name = db_name
        self.db_modified = False
        try:
            readline.read_history_file(self.histfile)
            readline.set_history_length(2048)
        except FileNotFoundError:
            pass

    def close(self):
        """
        Closes the current database connection if any and then closes the REPL
        """
        if self.connection is not None and self.db_modified:
            commit = input('Commit changes to the database? (y/n): ')
            if commit.lower() == 'y':
                print("Committing and closing...")
                self.connection.commit()
            self.connection.close()
        exit(0)

    def read(self):
        """
        The 'Read' portion of the REPL. Prompts the user for input and returns
        that input.
        """
        if self.db_name is not None:
            return input(f'({self.db_name})>>> ')
        else:
            return input(">>> ")

    def eval(self, cmd):
        """
        The 'eval' portion of the REPL. Calls other functions based on user
        input.
        """
        cmd = cmd.split()
        if self.connection is None:
            if cmd:
                if cmd[0] == 'open':
                    self.db_name = ' '.join(cmd[1:]).strip()
                    self.connection = connection_dialogue(cmd[1:])
                    return True
                elif cmd[0] == 'quit' or cmd[0] == 'exit':
                    return None
                else:
                    return self.print(f'"{" ".join(cmd)}" is not a command')
            else:
                return True
        else:
            if cmd[0] == 'quit' or cmd[0] == 'exit':
                self.close()
                return None
            else:
                if modifies_db(cmd):
                    self.db_modified = True
                # Yes, this is bad practice; TODO change this
                return self.connection.cursor().execute(' '.join(cmd))

    def print(self, obj):
        """
        The print portion of the REPL. Prints the output of the Eval'd input,
        or an error if the input was invalid.
        """
        if type(obj) is not str:
            try:
                # TODO Better printing function
                print(to_string(obj))
            except Exception as ex:
                print(ex)
        else:
            print(obj)

    def loop(self):
        """
        Prompts the user for input until it recieves a certain command, a
        catastrophic error occurs, a KeyboardInterrupt, or it reads an EOF
        character.
        """
        reading = True
        while reading:
            try:
                cmd = self.read()
                result = self.eval(cmd)
                if result is not None:
                    if type(result) is not bool:
                        self.print(result)
                else:
                    reading = False
                result = None
            except KeyboardInterrupt:
                self.close()
            except Exception as err:
                print(err)
                self.close()
