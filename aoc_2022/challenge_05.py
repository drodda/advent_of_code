#!/usr/bin/env python3

import copy
import re
import sys
import traceback
from common.utils import *


RE_MOVE = re.compile(r"move (\d+) from (\d+) to (\d+)")


def parse_input(test=False):
    """ Parse input file: return stack structure and list of moves as integers """
    stacks_s, moves_s = read_multilines(data_file_path_main(test=test))

    # Parse stacks into list of lists in reverse order
    n_stacks = int((len(stacks_s[-1]) + 1) / 4)
    stacks = []
    for i in range(n_stacks):
        _i = i * 4 + 1  # Index for stack text
        stack = [line[_i] for line in reversed(stacks_s[:-1]) if len(line) >= _i and line[_i] != " "]
        stacks.append(stack)

    # Parse moves into n, from, to
    moves = []
    for line in moves_s:
        m = RE_MOVE.match(line)
        if not m:
            log.error(f"Bad line: {line}")
            continue
        n, _from, _to = map(int, m.groups())
        moves.append((n, _from - 1, _to - 1))
    return stacks, moves


def solve(stacks, moves, smart=False):
    stacks = copy.deepcopy(stacks)
    for n, _from, _to in moves:
        moved = stacks[_from][-n:]
        if not smart:
            moved = reversed(moved)
        stacks[_from] = stacks[_from][:-n]
        stacks[_to].extend(moved)

    result = "".join([stack[-1] for stack in stacks])
    return result


def main():
    args = parse_args()
    stacks, moves = parse_input(test=args.test)

    log.always("Part 1:")
    result = solve(stacks, moves)
    log.always(result)

    log.always("Part 2:")
    result = solve(stacks, moves, smart=True)
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
