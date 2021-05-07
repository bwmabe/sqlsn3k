def modifies_db(cmd):
    """
    Checks if a query has the potential to modify the DB without actually
    checking if the DB was modified.
    """
    # TODO: Make this check more robust
    return cmd[0].lower() != "select"
