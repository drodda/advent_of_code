#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


DIRS = {
    "N": -1j,
    "E": 1+0j,
    "S": 1j,
    "W": -1+0j,
}


MOVES = {
    "N": "EW",
    "E": "SN",
    "S": "WE",
    "W": "NS",
    "START": "ES",
}


def solve(lines, move_min, move_max):
    data = {x + y * 1j: int(c) for y, line in enumerate(lines) for x, c in enumerate(line)}
    end = max(x.real for x in data) + max(y.imag for y in data) * 1j
    # Queue of nodes to explore: (cost, index, position, entry_direction)
    # index is included so nodes of similar cost can be compared, as position is complex
    to_explore = HeapQ([(0, 0, 0+0j, "START")])
    # Store minimum cost to explore a node entering from a given direction
    explored = collections.defaultdict(lambda: sys.maxsize)
    index = 0
    while to_explore:
        cost, _, pos, last_dir = to_explore.pop()
        if pos == end:
            return cost
        log.info(f"Exploring {pos:10.0f}\tfrom\t{last_dir}\t@ {cost}")
        for _dir in MOVES[last_dir]:
            _cost = cost
            for step in range(1, move_max+1):
                _pos = pos + DIRS[_dir] * step
                if _pos not in data:
                    break
                _cost += data[_pos]
                if step >= move_min:
                    if _cost < explored[(_pos, _dir)]:
                        index += 1
                        explored[(_pos, _dir)] = _cost
                        log.info(f"  Expanding into {_pos:10.0f}\tfrom\t{_dir}\t@ {_cost}")
                        to_explore.push((_cost, index, _pos, _dir))
    return None


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = solve(lines, 1, 3)
    log.always(result)

    log.always("Part 2:")
    result = solve(lines, 4, 10)
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
