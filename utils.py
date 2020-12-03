import argparse
import os
import sys


def read_lines(file_path, strip_empty=True):
    lines = open(file_path).read().splitlines()
    if strip_empty:
        lines = [line for line in lines if line]
    return lines


def read_list_int(file_path, strip=True):
    lines = read_lines(file_path, strip)
    return [int(line) for line in lines]


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


def data_file_path(test):
    # Get script name
    script_base, _ = os.path.splitext(os.path.basename(sys.argv[0]))
    data_file_suffix = "_test" if test else "_full"
    result = os.path.join("data", f"{script_base}{data_file_suffix}.txt")
    return result
