import os
import readline

import command_parser


class REPL:
    histfile = os.path.join(os.path.expanduser("~"), ".sqlsn3k_history")

    def __enter__(self):
        try:
            readline.read_history_file(self.histfile)
            readline.set_history_length(2048)
        except FileNotFoundError:
            pass

    def __exit__(self, type, value, tb):
        return


def print_output(out_string):
    if not out_string:
        out_string = ""
    lines = out_string.split('\n')
    no_lines = len(lines)
    size = os.get_terminal_size()
    height = size.lines
    width = size.columns
    longest_line = max(map(len, lines))
    to_print = list()
    if no_lines >= height:
        line_index = 0
        spacer_appended = False
        for line in lines:
            if line_index < 4:
                to_print.append(line)
            elif line_index > (no_lines - 5):
                to_print.append(line)
            elif not spacer_appended:
                margin = (" " * (width / 2)) - 3
                to_print.append(margin + "...")
                spacer_appended = True
    else:
        for line in lines:
            to_print.append(line)
    if longest_line >= width:
        to_print[:] = map(lambda s, w=width: s[:(w - 3)] + '...', to_print)
    for line in to_print:
        print(line)


def start_repl(user):
    with REPL():
        while True:
            try:
                cmd = input(user.prompt)
                cmd_output = command_parser.parse(cmd, user)
                print_output(cmd_output)
                user.update()
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except Exception as ex:
                print(ex)
                pass
