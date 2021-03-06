import argparse
import itertools
import logging
import os
import sys
import heapq


try:
    import ipdb as pdb
except ImportError:
    import pdb


# Get logger that will be used by all clients of this module, and add extra log levels and methods
log = logging.getLogger(sys.argv[0])


__all__ = [
    "SCRIPT_BASE", "data_file_path", "data_file_path_main", "parse_args", "trace",
    "log", "log_verbose", "log_never", "log_debug", "log_info", "log_warning", "log_always", "log_error",
    "ltrim", "rtrim", "str_reversed",
    "read_lines", "read_multilines", "read_list_int", "read_csv_int", "read_csv_int_multiline",
    "grouper",
    "HeapQ",
]


# Get script name
SCRIPT_BASE, _ = os.path.splitext(os.path.basename(sys.argv[0]))


def data_file_path(suffix, var="", ext="txt"):
    return os.path.join("data", f"{SCRIPT_BASE}{var}_{suffix}.{ext}")


def data_file_path_main(test):
    suffix = "test" if test else "full"
    return data_file_path(suffix)


def parse_args(args_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Use test data", action="store_true")
    parser.add_argument("--var", help="File variant to use", default="")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    if args_func:
        args_func(parser)
    args = parser.parse_args()

    log_level = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}.get(args.verbose, VERBOSE)
    logging.basicConfig(
        level=log_level,
        handlers=[logging.StreamHandler(sys.stdout)],
        format='%(message)s'
    )
    return args


# Export trace function for debugging
trace = pdb.set_trace


VERBOSE = logging.DEBUG - 1
logging.addLevelName(VERBOSE, "VERBOSE")
log.verbose = lambda msg, *args, **kwargs: log.log(VERBOSE, msg, *args, **kwargs)
ALWAYS = logging.CRITICAL
logging.addLevelName(ALWAYS, "ALWAYS")
log.always = log.critical
NEVER = logging.NOTSET - 1
logging.addLevelName(NEVER, "NEVER")
log.never = lambda msg, *args, **kwargs: log.log(NEVER, msg, *args, **kwargs)

# Export log functions
log_verbose = log.verbose
log_debug = log.debug
log_info = log.info
log_always = log.always
log_warning = log.warning
log_error = log.error
log_never = log.never

# Suppress verbose logging from libraries
logging.getLogger('asyncio').setLevel(logging.WARNING)


def rtrim(text, trim):
    """ remove suffix """
    if text.endswith(trim):
        return text[:-len(trim)]
    return text


def ltrim(text, trim):
    """ Remove prefix """
    if text.startswith(trim):
        return text[len(trim):]
    return text


def str_reversed(text):
    """ Reverse string, return string """
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
    lines = read_lines(file_path, strip)
    result = map(int, lines)
    if to_list:
        return list(result)
    return result


def _csv_to_int(line, to_list=False):
    result = map(int, line.strip().split(","))
    if to_list:
        return list(result)
    return result


def read_csv_int(file_path, to_list=False):
    """ Read a single-line CSV, return a list of strings """
    with open(file_path) as f:
        return _csv_to_int(f.read(), to_list=to_list)


def read_csv_int_multiline(file_path, to_list=False):
    """ Read a single-line CSV, return a list of lists of strings """
    with open(file_path) as f:
        for line in f:
            yield _csv_to_int(line, to_list=to_list)


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


class HeapQ:
    """ Wrapper around heapq from standard library """
    def __init__(self, items=None):
        self._h = []
        if items is not None:
            for item in items:
                self.push(item)

    def push(self, item):
        heapq.heappush(self._h, item)

    def pop(self):
        return heapq.heappop(self._h)

    def __bool__(self):
        return bool(self._h)
