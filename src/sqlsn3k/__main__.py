import sys

from sqlsn3k.repl import REPL


def parse_args(args):
    """
    Parses the command line arguments. For now, the only arg is `-d`, which
    allows the user to select which database file that they would like to use.
    More options might be added in the future or this option might be changed.
    """
    if args[0] == "-d":
        return ' '.join(args[1:]).strip()
    else:
        return None


def main():
    db_name = None
    con = None
    if len(sys.argv) > 1:
        args = parse_args(sys.argv)
        if args is not None:
            con = None
    repl = REPL(db_name, con)
    repl.loop()


main()
