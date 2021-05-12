def fit_row(row, width, ncols, interval):
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
    formatting_len = len(prefix + suffix + (delimiter * ncols))
    content_len = len(''.join(row))
    if (formatting_len + content_len) <= width:
        continuation = delimiter
    return_string = prefix
    new_list = list()
    midpoint = int(len(interval) / 2)
    lower_half = range(0, midpoint)
    upper_half = range(midpoint, len(interval))
    for i in lower_half:
        new_list.append(row[interval[i]])
    for i in upper_half:
        new_list.append(row[interval[i]])
    return_string += delimiter.join(new_list[:midpoint])
    return_string += continuation
    return_string += delimiter.join(new_list[midpoint:])
    return_string += suffix
    return return_string


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


def generate_intervals(elems):
    """
    Generates all possible permutations of lists that access elements from
    boths ends of a list without accessing the middle, and one permutation
    that accesses ALL elements of a list.
    """
    intervals = list()
    for i in range(0, elems):
        interval = list()
        if i <= int(elems / 2):
            for j in range(0, i):
                interval.append(j)
            if i == int(elems / 2) and (elems % 2) == 1:
                interval.append(int(elems / 2))
            for j in range(i - 1, -1, -1):
                interval.append(-1 * (j + 1))
        if interval:
            intervals.append(interval)
    return intervals


def best_fit(obj, max_val, nfields, fit_function):
    """
    Finds (nearly) the maximum amount of some object that can be displayed
    before truncation. Preserves the first n and last m elements and hides
    a subset of elements from the 'middle' of the object.
    """
    elems = len(obj)
    intervals = generate_intervals(elems)
    current_fit = list()
    last_best_fit = list()
    current_fit_str = None
    for interval in intervals:
        to_print = fit_function(obj, max_val, nfields, interval)
        if len(to_print) <= max_val:
            if len(to_print) > len(str(current_fit_str)):
                current_fit_str = to_print
                last_best_fit = current_fit
                current_fit = interval
    if current_fit is None and last_best_fit is None:
        return intervals[0]
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
