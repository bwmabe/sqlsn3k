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


def modifies_db(cmd):
    """
    Checks if a query has the potential to modify the DB without actually
    checking if the DB was modified.
    """
    # TODO: Make this check more robust
    return cmd[0].lower() != "select"
