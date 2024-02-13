#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *


def evaluate_str_1(s):
    # Must contain double letter
    if not re.search(r"(.)\1", s):
        return False
    # Must not contain ab|cd|pq|xy
    if re.search(r"(ab|cd|pq|xy)", s):
        return False
    # Must contain at least 3 vowels
    if len(re.findall(r"([aeiou])", s)) < 3:
        return False
    return True


def evaluate_str_2(s):
    # Must contain a duplicate pair of letters
    if not re.search(r"(..).*\1", s):
        return False
    # Must contain a duplicate letter separated by a single letter
    if not re.search(r"(.).\1", s):
        return False
    return True


def solve(lines, evaluator):
    result = 0
    for line in lines:
        if evaluator(line):
            log.debug(f"Match:   {line}")
            result += 1
        else:
            log.debug(f"No Match: {line}")
    return result


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    log.always("Part 1")
    result = solve(lines, evaluator=evaluate_str_1)
    log.always(result)

    log.always("Part 2")
    result = solve(lines, evaluator=evaluate_str_2)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
