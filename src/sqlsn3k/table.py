import shutil
import sqlite3


class Table:
    def __init__(self, cursor):
        raw = cursor.fetchall()
        self.header = raw[0].keys()
        self.ncols = len(self.header)
        rows = list(map(tuple, raw))
        temp_table = list()
        temp_table.append(tuple(self.header))
        temp_table += rows
        self.max_width = shutil.get_terminal_size().columns
        self.max_height = shutil.get_terminal_size().lines
        self.longests = self.longest_in_each_col(temp_table)
        self.table = self.snap_to_largest(temp_table)
        self.header = self.table[0]
        self.interval = self.find_best_fit(self.header, self.max_width,
                                           self.fit_row)

    def longest_in_each_col(self, table):
        """
        returns a List containing the lenght of the longest item in each column
        of a cursor. Column index corresponds to the index of the returned List
        """
        longests = [0 for i in range(0, self.ncols)]
        for i in range(0, self.ncols):
            if len(str(self.header[i])) > longests[i]:
                longests[i] = len(str(self.header[i]))
        for row in table:
            for i in range(0, self.ncols):
                if len(str(row[i])) > longests[i]:
                    longests[i] = len(str(row[i]))
        return longests

    def snap_to_largest(self, to_snap):
        """
        Snaps the width of each column of the table to the width of the
        largest element in the respective column.
        """
        new_table = list()
        for row in to_snap:
            new_row = list()
            for i in range(0, len(self.longests)):
                new_row.append(f'{str(row[i]):^{self.longests[i]}}')
            new_table.append(new_row)
        return new_table

    def fit_row(self, row, interval=None):
        """
        Prints a subset of columns in a row to fit within a certain width.
        This function might not be used in its current form. Should be changed
        to adapt to column widths being defined externally.
        """
        row = list(map(str, row))
        if interval is None:
            interval = self.interval
        prefix = '| '
        suffix = ' |'
        delimiter = ' | '
        continuation = ' ... '
        formatting_len = len(prefix + suffix + (delimiter * self.ncols))
        content_len = len(''.join(row))
        if (formatting_len + content_len) <= self.max_width:
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

    def generate_intervals(self, elems):
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

    def find_best_fit(self, obj, max_val, fit_function):
        """
        Finds (nearly) the maximum amount of some object that can be displayed
        before truncation. Preserves the first n and last m elements and hides
        a subset of elements from the 'middle' of the object.
        """
        if max_val is None:
            max_val = self.max_width
        elems = len(obj)
        intervals = self.generate_intervals(elems)
        current_fit = list()
        last_best_fit = list()
        current_fit_str = None
        for interval in intervals:
            to_print = fit_function(obj, interval)
            if len(to_print) <= max_val:
                if len(to_print) > len(str(current_fit_str)):
                    current_fit_str = to_print
                    last_best_fit = current_fit
                    current_fit = interval
        if current_fit is None and last_best_fit is None:
            return intervals[0]
        else:
            return current_fit

    def header_separator(self):
        """
        Returns a string to separate the header of a table from the body of
        the table.
        """
        separator = list()
        for i in self.longests:
            separator.append('-' * i)
        separator = self.fit_row(separator)
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
        header = self.fit_row(self.header)
        if ' ... ' in header:
            cols_truncated = self.ncols - len(self.interval)
            cols_truncated = f'[{cols_truncated} column(s) truncated]'
        lines.append(header)
        lines.append(self.header_separator())
        for row in self.table[1:]:
            lines.append(self.fit_row(row, interval=self.interval))
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
