#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *


RESULT_TEXT = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
""".strip()

RESULT = {k: int(v) for k, v in [line.split(": ") for line in RESULT_TEXT.splitlines()]}


def parse_input(lines):
    result = {}
    for line in lines:
        m = re.match(r"Sue (\d+): (.*)", line)
        if m:
            n, vals = m.groups()
            n = int(n)
            vals = {k: int(v) for k, v in [val.split(": ") for val in vals.split(", ")]}
            result[n] = vals
        else:
            log.error(f"Bad line: {line}")
    return result


def match_part1(vals):
    for k, v in vals.items():
        if v != RESULT[k]:
            return False
    return True


def match_part2(vals):
    for k, v in vals.items():
        if k in ["cats", "trees"]:
            if not v > RESULT[k]:
                return False
        elif k in ["pomeranians", "goldfish"]:
            if not v < RESULT[k]:
                return False
        elif v != RESULT[k]:
            return False
    return True


def solve(data, match_fn):
    for n, vals in data.items():
        if match_fn(vals):
            log.debug(f"Match: {vals} == {RESULT}")
            return n
    return None


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    data = parse_input(lines)

    log.always("Part 1")
    result = solve(data, match_part1)
    log.always(result)

    log.always("Part 2")
    result = solve(data, match_part2)
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
