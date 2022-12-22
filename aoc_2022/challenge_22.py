#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


DIRECTIONS = {
    "RIGHT": (1, 0),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "UP": (0, -1),
}

TURNS = {
    "RIGHT": {"L": "UP", "R": "DOWN"},
    "DOWN": {"L": "RIGHT", "R": "LEFT"},
    "LEFT": {"L": "DOWN", "R": "UP"},
    "UP": {"L": "LEFT", "R": "RIGHT"},
}

DIRECTION_VAL = {
    "RIGHT": 0,
    "DOWN": 1,
    "LEFT": 2,
    "UP": 3,
}


def parse_input(test=False):
    world, path_str = read_multilines(data_file_path_main(test=test))

    path = []
    s = ""
    for line in path_str:
        for c in line:
            if c.isnumeric():
                s += c
            else:
                if s:
                    path.append(int(s))
                    s = ""
                path.append(c)
    if s:
        path.append(int(s))

    # Pad world with spaces
    line_max = max([len(line) for line in world])
    world = [line + " " * (line_max - len(line)) for line in world]

    return world, path


def move_part1(world, x, y, _dir, n):
    _dx, _dy = DIRECTIONS[_dir]
    moved = 0
    _x = x
    _y = y
    while True:
        _y = (_y + _dy) % len(world)
        _x = (_x + _dx) % len(world[_y])
        if world[_y][_x] == "#":
            # End move
            log.debug(f"\tMove stopped")
            break
        if world[_y][_x] == ".":
            # Move: update x, y, increment move counter
            x, y = _x, _y
            moved += 1
            log.debug(f"\tMoved {moved}/{n}: {x, y}")
            if moved == n:
                break
    return x, y, _dir


def move_part2(world, x, y, _dir, n):
    _x = x
    _y = y
    for i in range(n):
        # Move in current direction
        _dx, _dy = DIRECTIONS[_dir]
        _y = _y + _dy
        _x = _x + _dx
        __dir = _dir
        if _x < 0 or _y < 0 or _y >= len(world) or _x >= len(world[_y]) or world[_y][_x] == " ":
            # Warp
            _x, _y, __dir = warp(x, y, _dir)
        if world[_y][_x] == "#":
            # End move
            log.debug(f"\tMove stopped")
            break
        # Move: update x, y
        x, y, _dir = _x, _y, __dir
        log.debug(f"\tMoved {i}/{n}: {x, y}")
    return x, y, _dir


# Part 2: When moving off the board warp to another location
# TODO: Work out how to do this programmatically, and apply to test input
def warp(x, y, _dir):
    if 150 <= y <= 199 and 0 <= x <= 49:  # surface 1
        if _dir == "RIGHT":
            return (y - 150) + 50, 149, "UP"
        elif _dir == "DOWN":
            return x + 100, 0, "DOWN"
        elif _dir == "LEFT":
            return (y - 150) + 50, 0, "DOWN"
    elif 100 <= y <= 149 and 0 <= x <= 49:  # surface 2
        if _dir == "LEFT":
            return 50, 49 - (y - 100), "RIGHT"
        elif _dir == "UP":
            return 50, x + 50, "RIGHT"
    elif 100 <= y <= 149 and 50 <= x <= 99:  # surface 3
        if _dir == "DOWN":
            return 49, (x - 50) + 150, "LEFT"
        elif _dir == "RIGHT":
            y_off = y - 100
            return 149, 49 - y_off, "LEFT"
    elif 50 <= y <= 99 and 50 <= x <= 99:  # surface 4
        if _dir == "LEFT":
            return (y - 50), 100, "DOWN"
        elif _dir == "RIGHT":
            return (y - 50) + 100, 49, "UP"
    elif 0 <= y <= 49 and 50 <= x <= 99:  # surface 5
        if _dir == "LEFT":
            return 0, 149 - y, "RIGHT"
        elif _dir == "UP":
            return 0, 150 + (x - 50), "RIGHT"
    elif 0 <= y <= 49 and 100 <= x <= 149:  # surface 6
        if _dir == "UP":
            return x - 100, 199, "UP"
        elif _dir == "RIGHT":
            return 99, 149 - y, "LEFT"
        elif _dir == "DOWN":
            return 99, (x - 100) + 50, "LEFT"
    raise ValueError(f"Unable to determine warp from {x, y} {_dir}")


def solve(world, path, move_fn):
    # Find start
    y = 0
    x = 0
    for x in range(len(world[0])):
        if world[y][x] == ".":
            break
    log.info(f"Start: {x, y}")
    _dir = "RIGHT"
    for i, instr in enumerate(path):
        if isinstance(instr, int):
            # Move
            log.debug(f"{i: 3d}: Moving {instr} from {x, y} {_dir}")
            x, y, _dir = move_fn(world, x, y, _dir, instr)
            log.info(f"{i: 3d}: Moved {instr}: {x, y} {_dir}")
        else:
            # Turn
            _dir = TURNS[_dir][instr]
            log.info(f"{i: 3d}: Turned {instr}: {_dir}")

    return 1000 * (y + 1) + 4 * (x + 1) + DIRECTION_VAL[_dir]


def main():
    args = parse_args()
    world, path = parse_input(test=args.test)

    log.always("Part 1:")
    result = solve(world, path, move_part1)
    log.always(result)

    if not args.test:
        log.always("Part 2:")
        result = solve(world, path, move_part2)
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
