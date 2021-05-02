import sqlite3

def parse_no_db(cmd, args, user):
    """
    Parses commands relating to locating and opening a database
    """
    cmd = cmd.lower()
    if cmd == "open" or cmd == "connect":
        if args:
            try:
                user.connect(args)
                return f"successfully connected to {' '.join(args)}"
            except Exception as e:
                return f"could not connect to {' '.join(args)}\nReason: {e}"
        else:
            return "No database specified"


def parse_query(query, db_connection):
    """
    Sends queries to and reads the results from the databse.
    """
    try:
        cur = db_connection.cursor()
        result = cur.execute(query)
    except sqlite3.DatabaseError as e:
        return e
    except TypeError:
        return "ERROR: no query given"
    except Exception as e:
        return f"Well this shouldn't happen...\n{e}"


def parse(command, user):
    """
    Parses the passed command and then performs the relevant action.
    Returns a str containing the output of the last command (if relevant) or
    an error message if the last command was not valid.
    Note: all commands are case insensitive
    """
    if command:
        split = command.split()
        cmd = split[0]
        args = split[1:]
        if user.db is None:
            result = parse_no_db(cmd, args)
        else:
            result = parse_query(command)
        # 'None' is used as the error value for 'parse_no_db' and 'query'
        if result is None:
            return f'command {cmd} not found'
        else:
            return result
    else:
        return None
