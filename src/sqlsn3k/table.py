import shutil
import sqlite3

from formatting import fit_row, longest_in_col, best_fit, snap_to_widest


class Table:
    def __init__(self, cursor):
        raw = cursor.fetchall()
        self.header = raw[0].keys()
        self.ncols = len(self.header)
        rows = list(map(tuple, raw))
        temp_table = list()
        temp_table.append(tuple(self.header))
        temp_table += rows
        self.width = shutil.get_terminal_size().columns
        self.height = shutil.get_terminal_size().lines
        self.longests = longest_in_col(temp_table, self.ncols, self.header)
        self.table = snap_to_widest(temp_table, self.longests)
        self.header = self.table[0]
        self.interval = best_fit(self.header, self.width, self.ncols, fit_row)

    def header_separator(self):
        """
        Returns a string to separate the header of a table from the body of
        the table.
        """
        separator = list()
        for i in self.longests:
            separator.append('-' * i)
        separator = fit_row(separator, self.width, self.ncols, self.interval)
        return separator

    def truncate_height(self, output):
        """
        Takes a List of Str and returns a truncated list that fits the display.
        """
        height = len(output)

    def printable(self):
        """
        Returns a list of strings that constitute a printable, human-readable,
        version of the table
        """
        cols_truncated = None
        lines = list()
        header = fit_row(self.header, self.width, self.ncols, self.interval)
        if ' ... ' in header:
            cols_truncated = self.ncols - len(self.interval)
            cols_truncated = f'[{cols_truncated} column(s) truncated]'
        lines.append(header)
        lines.append(self.header_separator())
        for row in self.table[1:]:
            lines.append(fit_row(row, self.width, self.ncols, self.interval))
        nlines = len(lines) - 2  # Remove header and separator from count
        lines.append(f'[Returned {nlines} Row(s) and {self.ncols} Column(s)]')
        if cols_truncated is not None:
            lines.append(cols_truncated)
        return lines


if __name__ == '__main__':
    con = sqlite3.connect('test.db')
    con.row_factory = sqlite3.Row
    table = Table(con.execute("SELECT * FROM info WHERE class='Sports Classics' ORDER BY lap_time ASC"))
    for line in table.printable():
        print(line)
