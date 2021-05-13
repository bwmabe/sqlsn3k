import shutil
import sqlite3

from formatting import fit_row, fit_table, longest_in_col, best_fit, snap_to_widest


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
        self.nrows = len(self.table)
        self.header = self.table[0]
        self.interval = best_fit(self.header, self.width, fit_row, self.ncols)

    def header_separator(self):
        """
        Returns a string to separate the header of a table from the body of
        the table.
        """
        separator = list()
        for i in self.longests:
            separator.append('-' * i)
        separator = fit_row(separator, self.width, self.interval, self.ncols)
        return separator

    def truncate_height(self, lines):
        """
        Takes a List of Str and returns a truncated list that fits the display.
        """
        return fit_table(lines, self.height, best_fit(lines, self.height - 5, fit_table))

    def printable(self):
        """
        Returns a list of strings that constitute a printable, human-readable,
        version of the table
        """
        cols_truncated = False
        rows_truncated = False
        lines = list()
        header = fit_row(self.header, self.width, self.interval, self.ncols)
        if ' ... ' in header:
            cols_truncated = self.ncols - len(self.interval)
            cols_truncated = f'[{cols_truncated} column(s) truncated]'
        lines.append(header)
        lines.append(self.header_separator())
        for row in self.table[1:]:
            lines.append(fit_row(row, self.width, self.interval, self.ncols))
        rowc = len(lines) - 2  # Don't count header, separator
        lines.append(f'[Returned {rowc} Row(s) and {self.ncols} Column(s)]')
        lines = self.truncate_height(lines)
        rowc = len(lines) - 2  # Update rowcount after height truncation
        if cols_truncated:
            lines.append(cols_truncated)
        if rowc < self.nrows:
            lines.append(f'[{self.nrows - rowc} Row(s) truncated]')
        return lines


if __name__ == '__main__':
    con = sqlite3.connect('test.db')
    con.row_factory = sqlite3.Row
    dims = shutil.get_terminal_size()

    def test_query(dims, connection, query):
        print(f'Test query: "{query}"')
        print(f'Dimensions: x:{dims.columns}, y:{dims.lines}')
        print('-' * dims.columns)
        table = Table(connection.execute(query))
        for line in table.printable():
            print(line)
        print('-' * dims.columns)

    test_query(dims, con, "SELECT * FROM info ORDER BY lap_time ASC")
    test_query(dims, con, "SELECT * FROM info WHERE class='Military'")
