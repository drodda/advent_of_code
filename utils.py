import argparse
import itertools
import logging
import os
import sys


try:
    import ipdb as pdb
except ImportError:
    import pdb


trace = pdb.set_trace


# Get logger that will be used by all clients of this module, and add extra log levels and methods
log = logging.getLogger(sys.argv[0])
VERBOSE = logging.DEBUG - 1
logging.addLevelName(VERBOSE, "VERBOSE")
log.verbose = lambda msg, *args, **kwargs: log.log(VERBOSE, msg, *args, **kwargs)
ALWAYS = logging.CRITICAL
logging.addLevelName(ALWAYS, "ALWAYS")
log.always = log.critical

# Export log functions
log_verbose = log.verbose
log_debug = log.debug
log_info = log.info
log_always = log.always


def rtrim(text, trim):
    """ remove suffix """
    l = len(trim)
    if text.endswith(trim):
        return text[:-l]
    return text


def ltrim(text, trim):
    l = len(trim)
    if text.startswith(trim):
        return text[l:]
    return text


def str_reversed(text):
    return text[::-1]


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


def parse_args(args_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Use test data", action="store_true")
    parser.add_argument("--var", help="File variant to use", default="")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    if args_func:
        args_func(parser)
    args = parser.parse_args()

    log_level = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}.get(args.verbose, VERBOSE)
    logging.basicConfig(level=log_level, format='%(message)s')

    return args


# Get script name
SCRIPT_BASE, _ = os.path.splitext(os.path.basename(sys.argv[0]))


def data_file_path(suffix, var="", ext="txt"):
    return os.path.join("data", f"{SCRIPT_BASE}{var}_{suffix}.{ext}")


def data_file_path_main(test):
    suffix = "test" if test else "full"
    return data_file_path(suffix)


def grouper(iterable, n=2, fillvalue=None, to_list=False):
    """ Group iterable into n-length chunks
        grouper('abcdefg', 3) --> ('a','b','c'), ('d','e','f'), ('g',None,None)
    """
    # Replicate iterable n times
    iterables = itertools.tee(iterable, n)
    # Slice iterables
    iterables_sliced = [itertools.islice(iterables[i], i, None, n) for i in range(n)]
    # Zip
    result = itertools.zip_longest(*iterables_sliced, fillvalue=fillvalue)
    if to_list:
        result = list(result)
    return result
