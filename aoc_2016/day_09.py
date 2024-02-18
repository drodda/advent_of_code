#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def expand(s: str, start: int = 0, end: int = None, recurse: bool = False):
    i = start
    result = 0
    if end is None:
        end = len(s)
    while i < end:
        if s[i] == "(":
            # Start of a group
            i1 = (s.index("x", i + 1))
            n_chars = int(s[i + 1:i1])
            i2 = s.index(")", i + 1)
            n_repeats = int(s[i1 + 1:i2])
            i = i2 + 1
            if recurse:
                group_end = i + n_chars
                while i < group_end:
                    _result, i = expand(s, start=i, end=group_end, recurse=recurse)
                    result += _result * n_repeats
            else:
                result += n_chars * n_repeats
                i += n_chars
        else:
            # Regular character
            result += 1
            i += 1
    return result, i


def solve(data, recurse=False):
    result, _ = expand(data, recurse=recurse)
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    for line in lines:
        log.debug(f"{line[:20]}...:")
        result = solve(line)
        log.always(result)
    log.debug("")

    log.always("Part 2:")
    for line in lines:
        log.debug(f"{line[:20]}...:")
        result = solve(line, recurse=True)
        log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
