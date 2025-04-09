#!/usr/bin/env python3
import collections
import functools
import sys
import traceback

from common.utils import *


def parse_input(args):
    data = list(read_lines(args.input))
    return data


NUMBER_PAD_LST = ("789", "456", "123", " 0A")
DIRECTION_PAD_LST = (" ^A", "<v>")


REPS_PART_1 = 2
REPS_PART_2 = 25

@functools.cache
def pad_coord(pad, sym):
    """Return coordinate (x, y) for sym in pad"""
    for y, row in enumerate(pad):
        for x, _sym in enumerate(row):
            if sym == _sym:
                return x, y
    raise ValueError(f"Sym {sym} does not exist")

@functools.cache
def pad_sym(pad, x, y):
    """Return sym in pad at (x,y)"""
    return pad[y][x]


@functools.cache
def pad_steps(pad, sym1, sym2):
    """Calculate steps to move in pad from sym1 to sym2"""
    x1, y1 = pad_coord(pad, sym1)
    x2, y2 = pad_coord(pad, sym2)
    dx = x2 - x1
    dy = y2 - y1
    syms_x = (">" if dx > 0 else "<") * abs(dx)
    syms_y = ("v" if dy > 0 else "^") * abs(dy)
    if pad_sym(pad, x2, y1) == " ":
        # Must go y before x
        return syms_y + syms_x
    if pad_sym(pad, x1, y2) == " ":
        # Must go x before y
        return syms_x + syms_y
    # Pre-optimised: Always move left before up/down (if possible)
    if dx < 0:
        return syms_x + syms_y
    # Must go up/down before right
    return syms_y + syms_x


@functools.cache
def solve_pad(pad, sequence, start="A"):
    """Calculate steps (as dictionary of step: count) to move in pad through sequence"""
    steps = collections.defaultdict(int)
    for dest in sequence:
        _sequence =  pad_steps(pad, start, dest) + "A"
        steps[_sequence] += 1
        start = dest
    return dict(steps)


def solve(lines, direction_reps):
    result = 0
    for line in lines:
        # Solve number pad
        steps = solve_pad(NUMBER_PAD_LST, line)
        # Solve direction pads
        for i in range(direction_reps):
            next_steps = collections.defaultdict(int)
            for sequence, count in steps.items():
                sequence_steps = solve_pad(DIRECTION_PAD_LST, sequence)
                for _sequence, _count in sequence_steps.items():
                    next_steps[_sequence] += count * _count
            steps = dict(next_steps)
        _result = 0
        for sequence, count in steps.items():
            _result += len(sequence) * count
        result += _result * int(line[:-1])
    return result


def main():
    args = parse_args()
    lines = parse_input(args)

    log.always("Part 1:")
    result = solve(lines, REPS_PART_1)
    log.always(result)

    log.always("Part 2:")
    result = solve(lines, REPS_PART_2)
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
