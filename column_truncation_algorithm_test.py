def print_subset(row, subset):
    """
    Prints a subset of a list defined by a list of integer list indices
    concatenates to a string a string.
    Prefixes, suffixes, and the delimiter are currently hardcoded, but could
    be changed to arguments.
    This function might not be used in its current form. Should be changed to
    adapt to column widths being defined externally.
    """
    prefix = '| '
    suffix = ' |'
    delimiter = ' | '
    continuation = ' ... '
    return_string = prefix
    new_list = list()
    midpoint = int(len(subset) / 2)
    lower_half = range(0, midpoint)
    upper_half = range(midpoint, len(subset))
    for i in lower_half:
        new_list.append(row[subset[i]])
    for i in upper_half:
        new_list.append(row[subset[i]])
    return_string += delimiter.join(new_list[:midpoint])
    return_string += continuation
    return_string += delimiter.join(new_list[midpoint:])
    return_string += suffix
    return return_string


def truncate_row(row, max_width):
    """
    Truncates a row (list of str) to a certain integer amount of characters.
    Includes a '...' if the entire list could not fit within the given width.
    """
    # TODO: account for the entire lenght of the row being able to fit within
    #       the gvien width.
    intervals = list()
    elems = len(row)
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
    current_fit = None
    last_best_fit = None
    for interval in intervals:
        to_print = print_subset(row, interval)
        if len(to_print) <= max_width:
            if len(to_print) > len(str(current_fit)):
                last_best_fit = current_fit
                current_fit = to_print
    if current_fit is None and last_best_fit is None:
        return print_subset(row, intervals[0])
    else:
        return current_fit


if __name__ == '__main__':
    test_list = ['aaa', 'bbbbbbbbbbbbb', 'ccccccc', 'd', 'eeeeee', 'ffff',
                 'ggggg', 'hhhhhhhhhhhhhhhhhhh', 'iiii', 'jjjjj', 'kkkkk']
    test_string = truncate_row(test_list, 60)
    print(test_string)
    print(len(test_string))
