#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_input(args):
    walls = set()
    start = None
    goal = None
    lines = read_lines(args.input)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            pos = (x, y)
            if c == "#":
                walls.add(pos)
            elif c == "S":
                start = pos
            elif c == "E":
                goal = pos
    return walls, start, goal


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

TURNS = {
    "^": ["<", ">"],
    "v": ["<", ">"],
    "<": ["^", "v"],
    ">": ["^", "v"],
}


def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def solve(walls, start, goal):
    _dir = ">"
    path_heads = HeapQ([(0, start, _dir, [start])])
    optimal_paths = {(start, _dir): 0}
    goal_paths = set()
    best_cost = None
    while path_heads:
        cost, pos, _dir, path = path_heads.pop()
        if cost > optimal_paths.get((pos, _dir), sys.maxsize):
            # Sub-optimal route
            continue
        optimal_paths[(pos, _dir)] = cost
        if pos == goal:
            if best_cost is not None and cost > best_cost:
                break
            best_cost = cost
            goal_paths.update(path)

        # Move forward
        _pos = move(pos, _dir)
        _cost = cost + 1
        if _pos not in walls:
            path_heads.push((cost + 1, _pos, _dir, path + [_pos]))
        # Turn and move
        for __dir in TURNS[_dir]:
            # Only bother turning if there is a path in that direction
            _pos = move(pos, __dir)
            if _pos not in walls:
                path_heads.push((cost + 1001, _pos, __dir, path + [_pos]))
    return best_cost, len(goal_paths)


def main():
    args = parse_args()
    walls, start, goal = parse_input(args)

    result_1, result_2 = solve(walls, start, goal)

    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
