# SQLSn3k
Pronounced: *sequel-snek*

**An Alternative SQLite3 REPL written in Python**

## About
SQLSn3k is an alternative SQLite3 REPL/shell written in Python. It was made because I got really frustrated/annoyed with the default `sqlite3` REPL and its lack of features. 

### Features
* Indicator for the currently opened database
* Adds support for the `home`, `end`, and arrow keys; along with emacs-like cursor movement!
* History

### Dependencies
It only depends on packages in the standard library.

`argparse, command_parser, os, readline, shutil, sqlite3, sys`

## TODO
* Add height truncation when displaying the result of a query
* Fix `index out of range` when a query returns no results
* Add info about number of rows affected (and maybe tables?) to all non-mutating queries
* Finish implementing history support
  - Figure out how to get `y/n` prompts to not record

### Wishlist
* Tab completion
* Syntax highlighting
* Support for "real" SQL-like RDBMSes
