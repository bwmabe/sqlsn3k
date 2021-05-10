import sqlite3

from table import Table


def process_row(row, first=False):
    """
    Converts a sqlite3.Row object to a string. A boolean is passed to indicate
    if the supplied row is the first or only row in a list() of rows.
    """
    heading = ''
    if first:
        heading = ' '.join(row.keys()) + '\n'
    content = ' '.join(map(str, row))
    return heading + content


def pretty_print(rct):
    """
    Pretty-prints either a sqlite3.Row or Cursor object.
    'rc' stands for row cursor as it could be either.
    Function is designed weirdly because Python doesn't have overloading
    """
    T = type(rct)
    if T is sqlite3.Row:
        return process_row(rct, first=True)
    elif T is sqlite3.Cursor:
        table = rct.fetchall()
        content = list()
        content.append(process_row(table[0], first=True))
        content += list(map(process_row, table[1:]))
        return '\n'.join(content)
    elif T is Table:
        return '\n'.join(rct.printable())


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
        for item in not_string:
            if item is None:
                printable_list.append('')
            else:
                printable_list.append(str(item))
        return list_delimiter.join(printable_list)
    elif T is sqlite3.Row or T is sqlite3.Cursor or T is Table:
        return pretty_print(not_string)
    else:
        return str(not_string)
