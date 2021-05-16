import sqlite3

import table


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
        tbl = rct.fetchall()
        content = list()
        content.append(process_row(tbl[0], first=True))
        content += list(map(process_row, tbl[1:]))
        return '\n'.join(content)
    elif T is table.Table:
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
        try:
            printable_list = list()
            for item in not_string:
                if item is None:
                    printable_list.append('')
                else:
                    printable_list.append(str(item))
            return list_delimiter.join(printable_list)
        except Exception as ex:
            print(f'formatting:to_string:list: {ex}')
    elif T is sqlite3.Row or T is sqlite3.Cursor or T is table.Table:
        try:
            return pretty_print(not_string)
        except Exception as ex:
            print(f'formatting:to_string:rct: {ex}')
    else:
        return str(not_string)


def insert_at_midpoint(item, iterable):
    """
    Inserts an item at the index of the midpoint of a list
    Returns that list with the item inserted
    """
    midpoint = int(len(iterable) / 2)
    iterable.insert(midpoint, item)
    return iterable


def fit_row(row, width, interval, nfields=None):
    """
    Prints a subset of columns in a row to fit within a certain width.
    This function might not be used in its current form. Should be changed
    to adapt to column widths being defined externally.
    """
    row = list(map(str, row))
    prefix = '| '
    suffix = ' |'
    delimiter = ' | '
    continuation = ' ... '
    formatting_len = len(prefix + suffix + (delimiter * nfields))
    content_len = len(''.join(row))
    if (formatting_len + content_len) <= width:
        continuation = delimiter
    new_list = list()
    for i in interval:
        new_list.append(row[i])
    new_list = insert_at_midpoint(continuation, new_list)
    return_string = prefix
    return_string += delimiter.join(new_list)
    return_string += suffix
    return return_string


def fit_table(table, height, interval, nfields=None):
    """
    Takes a list of rows, a desired height, and an interval to see if the list
    will fit within the specified height.
    Doesn't truncate if the desired height is less than 15 lines tall
    Subtracts 5 lines from the given to make sure that additional formatting
    elements and information lines can fit on the screen
    """
    if height <= 15:
        return table
    new_table = [table[i] for i in interval]
    old_height = len(table)
    width = len(table[0])
    if old_height >= height:
        continuation = '...'
        new_table = insert_at_midpoint(f'{continuation:^{width}}', new_table)
    return new_table


def longest_in_col(table, ncols, header=None):
    """
    returns a List containing the lenght of the longest item in each column
    of a cursor. Column index corresponds to the index of the returned List
    """
    longests = [0 for i in range(0, ncols)]
    if header is not None:
        for i in range(0, ncols):
            if len(str(header[i])) > longests[i]:
                longests[i] = len(str(header[i]))
    for row in table:
        for i in range(0, ncols):
            if len(str(row[i])) > longests[i]:
                longests[i] = len(str(row[i]))
    return longests


def generate_intervals(nelements):
    """
    Generates all possible permutations of lists that access elements from
    boths ends of a list without accessing the middle, and one permutation
    that accesses ALL elements of a list.
    """
    intervals = list()
    for i in range(0, nelements):
        interval = list()
        if i <= int(nelements / 2):
            for j in range(0, i):
                interval.append(j)
            if i == int(nelements / 2) and (nelements % 2) == 1:
                interval.append(int(nelements / 2))
            for j in range(i - 1, -1, -1):
                interval.append(-1 * (j + 1))
        if interval:
            intervals.append(interval)
    return intervals


def best_fit(obj, max_val, fit_function, nfields=None):
    """
    Finds (nearly) the maximum amount of some object that can be displayed
    before truncation. Preserves the first n and last m elements and hides
    a subset of elements from the 'middle' of the object.
    """
    intervals = generate_intervals(len(obj))
    current_fit = list()
    current_fit_obj = None
    for interval in intervals:
        fitted = fit_function(obj, max_val, interval, nfields=nfields)
        T = type(fitted)
        L = None
        if fitted is not None:
            L = len(fitted)
        else:
            L = max_val + 1
        if L <= max_val:
            if T is str:
                if L > len(str(current_fit_obj)):
                    current_fit_obj = fitted
                    current_fit = interval
            elif T is list:
                if current_fit_obj is None:
                    current_fit_obj = list()
                if L > len(list(current_fit_obj)):
                    current_fit_obj = fitted
                    current_fit = interval
    if current_fit_obj is None:
        return intervals[-1]
    else:
        return current_fit


def snap_to_widest(to_snap, widests):
    """
    Snaps the width of each column of the table to the width of the
    largest element in the respective column.
    """
    new_table = list()
    for row in to_snap:
        new_row = list()
        for i in range(0, len(widests)):
            new_row.append(f'{str(row[i]):^{widests[i]}}')
        new_table.append(new_row)
    return new_table
