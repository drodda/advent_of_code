import argparse
import os
import sys


def rtrim(text, trim):
    """ removesuffix """
    l = len(trim)
    if text.endswith(trim):
        return text[:-l]
    return text


def ltrim(text, trim):
    l = len(trim)
    if text.startswith(trim):
        return text[l:]
    return text


def read_lines(file_path, strip_empty=True, to_list=False):
    """ Read a file, yield a list of lines.
        strip_empty will remove empty lines
        to_list will return a list instead of a generator
    """
    line_gen = _read_lines(file_path, strip_empty)
    if to_list:
        return list(line_gen)
    return line_gen


def _read_lines(file_path, strip_empty=True):
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


def read_list_int(file_path, strip=True, to_list=False):
    """ Read a file of integers, one per line
        strip will remove empty lines
        to_list will return a list instead of a generator
    """
    lines = read_lines(file_path, strip, to_list)
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
__DEBUG_VERBOSE = False


def print_debug(text=""):
    if __DEBUG_PRINT:
        print(text)


def print_verbose(text=""):
    if __DEBUG_VERBOSE:
        print(text)


def global_set(name, val):
    globals()[name] = val


def parse_args(args_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Use test data", action="store_true")
    parser.add_argument("-d", "--debug", help="Debug output", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose Debug output", action="store_true")
    if args_func:
        args_func(parser)
    args = parser.parse_args()
    global_set("__DEBUG_PRINT", args.debug or args.verbose)
    global_set("__DEBUG_VERBOSE", args.verbose)
    return args


# Get script name
SCRIPT_BASE, _ = os.path.splitext(os.path.basename(sys.argv[0]))


def data_file_path(suffix, var="", ext="txt"):
    return os.path.join("data", f"{SCRIPT_BASE}{var}_{suffix}.{ext}")


def data_file_path_main(test):
    suffix = "test" if test else "full"
    return data_file_path(suffix)
