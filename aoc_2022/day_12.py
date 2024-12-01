#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def solve(data, starts, end):
    """ Find the shortest path between starts and end of data, ascending at most 1 each time """
    # Use Dijkstra search
    explored = set()
    q = HeapQ([(0, start) for start in starts])
    while q:
        cost, pos = q.pop()
        if pos in explored:
            continue
        if pos == end:
            return cost
        explored.add(pos)
        x, y = pos
        height = data[y][x]
        for _x, _y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= _x < len(data[0]) and 0 <= _y < len(data):
                _height = data[_y][_x]
                if _height <= height + 1:
                    q.push((cost + 1, (_x, _y)))
    return None


def main():
    args = parse_args()
    data = read_lines(args.input, to_list=True)

    # Find start and end coordinates in data
    start = None
    end = None
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == "S":
                start = x, y
            if c == "E":
                end = x, y
    # Convert to integer height
    data = [list(map(lambda x: ord(x) - ord("a"), line.replace("S", "a").replace("E", "z"))) for line in data]

    log.always("Part 1:")
    result = solve(data, [start], end)
    log.always(result)

    log.always("Part 2:")
    # Find all possible start locations
    starts = []
    for y, line in enumerate(data):
        for x, v in enumerate(line):
            if v == 0:
                starts.append((x, y))
    result = solve(data, starts, end)
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
