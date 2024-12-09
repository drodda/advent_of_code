#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


TURNS_RIGHT = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^"
}

def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def find_start(grid):
    for pos, sym in grid.items():
        if sym in DIRECTIONS:
            return pos, sym
    log.error(f"Unable to find start")
    return None, None


def simulate(grid, start=None):
    if start is None:
        pos, _dir = find_start(grid)
    else:
        pos, _dir = start
    visited_pos_dirs = set()
    visited = set()
    loop = False
    while True:
        if (pos, _dir) in visited_pos_dirs:
            loop = True
            break
        visited_pos_dirs.add((pos, _dir))
        visited.add(pos)
        _pos = move(pos, _dir)
        if _pos not in grid:
            break
        if _pos not in grid or grid[_pos] == "#":
            # Wall: or edge of grid: turn
            _dir = TURNS_RIGHT[_dir]
        else:
            pos = _pos
    return visited, loop


def solve_part1(grid):
    visited, _ = simulate(grid)
    return len(visited)


def solve_part2(grid):
    start = find_start(grid)
    start_pos, _ = start
    visited, _ = simulate(grid, start)
    result = 0
    for _pos in visited:
        if _pos != start_pos:
            _grid = grid.copy()
            _grid[_pos] = "#"
            _, loop = simulate(_grid, start)
            if loop:
                result += 1
    return result


def main():
    args = parse_args()
    data = list(read_lines(args.input))
    # Normalise grid into dictionary of symbols
    grid = {(x, y): sym for y, row in enumerate(data) for x, sym in enumerate(row)}

    log.always("Part 1:")
    result = solve_part1(grid)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(grid)
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
