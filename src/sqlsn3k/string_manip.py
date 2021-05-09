import sqlite3


def longest_col_in_row(row):
    longest = (None, 0)
    for elem in row:
        curr = (elem, len(str(elem)))
        if curr[1] > longest[1]:
            longest = curr
    return curr


def longest_in_each_col(cursor):
    """
    returns a List containing the lenght of the longest item in each column
    of a cursor. Column index corresponds to the index of the returned List.
    """
    first_row = cursor.fetchone()
    ncols = len(first_row)
    rows = [first_row]
    longests = [0 for i in range(0, ncols)]
    for row in cursor.fetchall():
        rows.append(row)
    for row in rows:
        for i in range(0, ncols):
            if len(str(row[i])) > longests[i]:
                longests[i] = len(str(row[i]))
    return longests


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
        for item in not_string:
            if item is None:
                printable_list.append('')
            else:
                printable_list.append(str(item))
        return list_delimiter.join(printable_list)
    elif T is sqlite3.Row or T is sqlite3.Cursor:
        return pretty_print(not_string)
    else:
        return str(not_string)


if __name__ == '__main__':
    con = sqlite3.connect('test.db')
    con.row_factory = sqlite3.Row
    cur = con.execute("SELECT * FROM info")
    head = con.execute("SELECT * FROM info").fetchone().keys()
    longests = longest_in_each_col(cur)
    for i in range(0, 26):
        print(f'{head[i]}, {longests[i]}')
