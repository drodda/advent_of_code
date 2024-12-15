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
log = logging.getLogger("main")


__all__ = [
    "parse_args", "trace", "log",
    "ltrim", "rtrim", "str_reversed",
    "read_lines", "read_multilines", "read_list_int", "read_csv_int", "read_csv_int_multiline",
    "grouper",
    "make_hashable", "full_hash",
    "HeapQ", "SetHeapQ",
]


ALL_PARTS = (1, 2)


def parse_args(args_func=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file")
    parser.add_argument('-p', '--part', type=int, choices=ALL_PARTS, default=None)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-t', '--test', action='store_true')
    if args_func:
        args_func(parser)
    args = parser.parse_args()

    args.part1 = args.part in (None, 1)
    args.part2 = args.part in (None, 2)

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
ALWAYS = logging.CRITICAL + 10
logging.addLevelName(ALWAYS, "ALWAYS")
log.always = log.critical
NEVER = logging.NOTSET - 1
logging.addLevelName(NEVER, "NEVER")
log.never = lambda msg, *args, **kwargs: log.log(NEVER, msg, *args, **kwargs)


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


def _csv_to_int(line, sep=",", to_list=False):
    result = map(int, line.strip().split(sep))
    if to_list:
        return list(result)
    return result


def read_csv_int(file_path, sep=",", to_list=False):
    """ Read a single-line CSV, return a list of strings """
    with open(file_path) as f:
        return _csv_to_int(f.read(), sep=sep, to_list=to_list)


def read_csv_int_multiline(file_path, sep=",", to_list=False):
    """ Read a single-line CSV, return a list of lists of strings """
    with open(file_path) as f:
        for line in f:
            yield _csv_to_int(line, sep=sep, to_list=to_list)


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


def make_hashable(v):
    if isinstance(v, dict):
        return hash(tuple((make_hashable(_k), make_hashable(_v)) for _k, _v in sorted(v.items())))
    elif isinstance(v, list):
        return hash(tuple(make_hashable(_v) for _v in v))
    else:
        return v


def full_hash(v):
    return hash(make_hashable(v))


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


class SetHeapQ(HeapQ):
    """ HeapQ implementation that keeps track of items in a set, implements __contains__ via set
        NOTE: HeapQ can not contain the same item more than once
    """
    def __init__(self, items=None):
        self._set = set()
        super().__init__(items=items)

    def push(self, item):
        item_hash = hash(item)
        if item_hash not in self._set:
            super().push(item)
            self._set.add(item_hash)

    def pop(self):
        item = super().pop()
        item_hash = hash(item)
        if item_hash in self._set:
            self._set.remove(item_hash)
        return item

    def __contains__(self, item):
        return item in self._set
