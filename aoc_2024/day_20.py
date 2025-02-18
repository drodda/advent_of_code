#!/usr/bin/env python3

import collections
import sys
import traceback

from common.utils import *


def parse_input(args):
    start = None
    end = None
    maze = set()
    for y, line in enumerate(read_lines(args.input)):
        for x, c in enumerate(line):
            pos = (x, y)
            if c == "S":
                start = pos
            elif c == "E":
                end = pos
                maze.add(pos)
            elif c == ".":
                maze.add(pos)
    return start, end, maze


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def move(pos, _dir, dist=1):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0] * dist, pos[1] + DIRECTIONS[_dir][1] * dist


def solve_maze(start, end, maze):
    distance_to_end = {end, }
    path_heads = HeapQ([(0, end, [end])])  # Cost, position, cheated, explored path
    while path_heads:
        cost, pos, path = path_heads.pop()
        for _dir in DIRECTIONS:
            _pos = move(pos, _dir)
            _cost = cost + 1
            _path = [_pos] + path
            if _pos in distance_to_end:
                continue
            distance_to_end.add(_pos)
            if _pos == start:
                return _path
            if _pos in maze:
                path_heads.push((_cost, _pos, _path))


def cheat_fn_part1(pos):
    for _dir in DIRECTIONS:
        yield move(pos, _dir, 2), 2


def cheat_fn_part2(pos):
    for i in range(-20, 21):
        _pos = move(pos, "^", i)
        for j in range(-20 + abs(i), 21 - abs(i)):
            yield move(_pos, ">", j), abs(i) + abs(j)


def solve(start, end, maze, threshold, cheat_fn):
    path = solve_maze(start, end, maze)
    path_cost = {pos: cost for cost, pos in enumerate(reversed(path))}

    result = 0
    results = collections.defaultdict(int)
    for pos in path:
        cost = path_cost[pos]
        # Attempt to cheat
        for _pos, steps in cheat_fn(pos):
            if _pos != pos and _pos in path:
                delta = cost - path_cost[_pos] - steps
                if delta >= threshold:
                    log.debug(f"Cheat at {pos} {cost} saves {delta}")
                    result += 1
                    results[delta] += 1
    for delta, count in sorted(results.items()):
        log.info(f"{count} cheats save {delta}")
    return result


def main():
    args = parse_args()
    start, end, maze = parse_input(args)

    log.always("Part 1:")
    threshold = 0 if args.test else 100
    result = solve(start, end, maze, threshold, cheat_fn_part1)
    log.always(result)

    log.always("Part 2:")
    threshold = 50 if args.test else 100
    result = solve(start, end, maze, threshold, cheat_fn_part2)
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
