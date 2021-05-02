import sys
import argparse

import repl
import db_user


def parse_args(argv):
    parser = argparse.ArgumentParser("Open and edit SQLite3 Databases")
    parser.add_argument("-d", metavar="DATABSE", type=str,
                        help="filename or path of the database to open")
    return parser.parse_args(argv[1:])


def main(argv):
    args = parse_args(argv)
    user = db_user.DBUser()
    if args.d:
        user.connect(args.d)
    repl.start_repl(user)


main(sys.argv)
