#!/usr/bin/env python3
import collections
import contextlib
import sys
import traceback
from common.utils import *


DIRS = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

MOVES = {
    "\\": {
        "N": "W",
        "W": "N",
        "S": "E",
        "E": "S",
    },
    "/": {
        "N": "E",
        "E": "N",
        "S": "W",
        "W": "S",
    },
    "|": {
        "N": "N",
        "S": "S",
        "E": "NS",
        "W": "NS",
    },
    "-": {
        "N": "EW",
        "S": "EW",
        "E": "E",
        "W": "W",
    },
    ".": {_dir: _dir for _dir in DIRS.keys()}
}


def move(data, y, x, _dir):
    dy, dx = DIRS[_dir]
    _y = y + dy
    _x = x + dx
    if not ((0 <= _y < len(data)) and (0 <= _x < len(data[_y]))):
        raise ValueError(f"Out of bounds: {_y},{_x} ({_dir} from {y},{x})")
    return _y, _x


def energise(data, y, x, _dir):
    explored = {(y, x, _dir), }
    to_explore = collections.deque(explored)
    while to_explore:
        pos = to_explore.pop()
        y, x, _dir = pos
        # log.info(f"Exploring ({y, x}) going {_dir}")
        sym = data[y][x]
        moves = MOVES[sym][_dir]
        for __dir in moves:
            with contextlib.suppress(ValueError):
                _y, _x = move(data, y, x, __dir)
                _pos = (_y, _x, __dir)
                if _pos not in explored:
                    to_explore.append(_pos)
                    explored.add(_pos)
    return len(set([(y, x) for y, x, _ in explored]))


def solve_part1(data):
    result = 0
    y_max = len(data)
    x_max = len(data[0])
    # Enter grid horizontally
    for y in range(y_max):
        for x, _dir in [(0, "E"), (x_max - 1, "W")]:
            _result = energise(data, y, x, _dir)
            log.info(f"{y, x} going {_dir} = {_result}")
            result = max(result, _result)
    # Enter grid vertically
    for x in range(x_max):
        for y, _dir in [(0, "S"), (y_max - 1, "N")]:
            _result = energise(data, y, x, _dir)
            log.info(f"{y, x} going {_dir} = {_result}")
            result = max(result, _result)
    return result


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)

    log.always("Part 1:")
    result = energise(data, 0, 0, "E")
    log.always(result)

    log.always("Part 2:")
    result = solve_part1(data)
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
