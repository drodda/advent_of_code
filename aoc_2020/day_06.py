#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def ascii_to_num(c):
    return ord(c) - ord("a")


MAX_VAL = ascii_to_num("z") + 1


def parse_input(filename):
    lines = read_lines(filename, strip_empty=False)
    entries = []
    entry = []
    for line in lines:
        if not line:
            # Flush entry
            if entry:
                entries.append(entry)
            entry = []
        else:
            entry.append(line)
    if entry:
        entries.append(entry)
    return entries


def flatten_input(entries_text):
    entries = []
    for entry_text in entries_text:
        n = len(entry_text)
        entry = np.zeros((n, MAX_VAL), dtype=np.bool)
        for i, line in enumerate(entry_text):
            for c in line:
                entry[i, ascii_to_num(c)] = True
        entries.append(entry)
    return entries


def main():
    args = parse_args()

    entries_text = parse_input(args.input)
    entries = flatten_input(entries_text)

    any_count = 0
    all_count = 0
    for i, entry in enumerate(entries):
        n = len(entry)
        entry_sum = sum(entry)
        entry_any_count = sum(entry_sum > 0)
        any_count += entry_any_count
        entry_all_count = sum(entry_sum >= n)
        all_count += entry_all_count
        log.debug(f"{i}: {entry_any_count}, {entry_all_count}")

    log.always("Part 1:")
    log.always(any_count)
    log.always("Part 2:")
    log.always(all_count)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
