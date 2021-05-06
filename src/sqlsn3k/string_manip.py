import sqlite3


from sqlite_helpers import process_row


def pretty_print(rc):
    """
    Pretty-prints either a sqlite3.Row or Cursor object.
    'rc' stands for row cursor as it could be either
    """
    T = type(rc)
    if T is sqlite3.Row:
        return process_row(rc, first=True)
    elif T is sqlite3.Cursor:
        rows = rc.fetchall()
        content = list()
        content.append(process_row(rows[0], first=True))
        content += list(map(process_row, rows[1:]))
        return '\n'.join(content)


def to_string(not_string, list_delimiter=', '):
    """
    Handles converting multiple arbitrary non-str datatypes into str's for
    printing. Also pretty-prints SQLite query output.
    """
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
    elif T is sqlite3.Row or T is sqlite3.Cursor:
        return pretty_print(not_string)
    else:
        return str(not_string)
