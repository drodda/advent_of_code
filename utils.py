import argparse
import os
import sys


def rtrim(text, trim):
    """ removesuffix """
    l = len(trim)
    if text.endswith(trim):
        return text[:-l]
    return text


def read_lines(file_path, strip_empty=True):
    """ Read a file, yield a list of lines.
        Remove empty lines if strip_empty
    """
    with open(file_path) as f:
        for line in f:
            line = line.rstrip("\r\n")
            if strip_empty:
                if not line:
                    continue
            yield line


def read_list_int(file_path, strip=True):
    """ Read a file of integers, one per line """
    lines = read_lines(file_path, strip)
    return map(int, lines)


def read_multilines(file_path, join=False, join_str=" "):
    """ Read a file of lines separated by blank lines
        Return an array of arrays of line groups
    """
    item = []
    for line in read_lines(file_path, False):
        line = line.rstrip("\r\n")
        if line:
            item.append(line)
        else:
            if item:
                if join:
                    item = join_str.join(item)
                yield item
                item = []
    if item:
        if join:
            item = join_str.join(item)
        yield item


__DEBUG_PRINT = False


def print_debug(text):
    if __DEBUG_PRINT:
        print(text)


def parse_args(args_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Use test data", action="store_true")
    parser.add_argument("--debug", help="Debug output", action="store_true")
    if args_func:
        args_func(parser)
    args = parser.parse_args()
    global __DEBUG_PRINT
    __DEBUG_PRINT = args.debug
    return args


# Get script name
SCRIPT_BASE, _ = os.path.splitext(os.path.basename(sys.argv[0]))


def data_file_path(suffix, var="", ext="txt"):
    return os.path.join("data", f"{SCRIPT_BASE}{var}_{suffix}.{ext}")


def data_file_path_main(test):
    suffix = "test" if test else "full"
    return data_file_path(suffix)
