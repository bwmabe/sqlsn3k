import readline
import sqlite3
import os
import sys


class REPL:
    histfile = os.path.join(os.path.expanduser("~"), ".sqlsn3k_history")

    def __init__(self, db_name=None, database_connection=None):
        self.connection = database_connection
        self.db_name = db_name
        try:
            readline.read_history_file(self.histfile)
            readline.set_history_length(2048)
        except FileNotFoundError:
            pass

    def close(self):
        if self.connection is not None:
            commit = input('Commit changes to the database? (y/n): ')
            if commit.lower() == 'y':
                print("Committing and closing...")
                self.connection.commit()
            self.connection.close()
        exit(0)

    def read(self):
        if self.db_name is not None:
            return input(f'({self.db_name})>>> ')
        else:
            return input(">>> ")

    def eval(self, cmd):
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
                # Yes, this is bad practice; TODO change this
                return self.connection.cursor().execute(' '.join(cmd))

    def print(self, obj):
        if type(obj) is sqlite3.Cursor:
            try:
                # TODO Better printing function
                rows = obj.fetchall()
                if rows:
                    print(rows[0].keys())
                    for row in rows:
                        print(to_string(row))
            except Exception as ex:
                print(ex)
        else:
            print(str(obj))

    def loop(self):
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


def to_string(not_string, list_delimiter=', '):
    T = type(not_string)
    if not_string is None:
        return ''
    elif T is list or T is tuple or T is set:
        printable_list = list()
        for item in T:
            if item is None:
                printable_list.append('')
            else:
                printable_list.append(str(item))
        return list_delimiter.join(printable_list)
    elif T is sqlite3.Row:
        return ', '.join(map(str, not_string))
    else:
        return str(not_string)


def parse_args(args):
    if args[0] == "-d":
        return ' '.join(args[1:]).strip()
    else:
        return None


def connect(path):
    try:
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        return connection
    except Exception as e:
        print(f'Error opening database "{path}":\n{e}')
        return None


def connection_dialogue(path):
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


if __name__ == "__main__":
    db_name = None
    con = None
    if len(sys.argv) > 1:
        args = parse_args(sys.argv)
        if args is not None:
            con = connect(args)
        else:
            con = None
    repl = REPL(db_name, con)
    repl.loop()
