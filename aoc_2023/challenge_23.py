#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


DIRS = {
    "^": -1j,
    ">": 1+0j,
    "v": 1j,
    "<": -1+0j,
}

NEXT_DIR = {
    **DIRS,
    ".": list(DIRS.values()),
}

PATH_SYM = list(NEXT_DIR.keys())

LABEL_START = "START"
LABEL_END = "START"


def parse(data):
    points = {}
    start = None
    end = None
    # Parse input, generate list of points that are path
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            pos = x + y * 1j
            if c in PATH_SYM:
                points[pos] = c
                if y == 0:
                    start = pos
                if y == len(data) - 1:
                    end = pos

    # Calculate points that are network nodes
    nodes = {
        LABEL_START: start,
        LABEL_END: end
    }
    n_nodes = 0
    for point in sorted(points, key=lambda v: (v.imag, v.real)):
        if sum([(point + delta) in points for delta in DIRS.values()]) >= 3:
            log.debug(f"Node: {point}")
            label = chr(ord("A") + n_nodes)
            n_nodes += 1
            nodes[label] = point
    print(nodes)

    point_to_node = {v: k for k, v in nodes.items()}

    # Calculate network
    network = {}
    for start_point in nodes:
        for _dir, delta in DIRS.items():
            point = start_point + delta
            path_length = 1
            if point not in points:
                continue
            # Follow path to a new node
            while point not in nodes:
                neighbours = []
                for next_dir, delta in DIRS.items():
                    if next_dir == _dir:
                        continue
                    next_point = point + delta
                    if

    return points, start, end


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)
    grid, start, end = parse(data)

    # print(grid)
    # print(start)
    # print(end)

    log.always("Part 1:")
    # result = len(simulate(pts, {start_pt, }, 6 if args.test else 64))
    # log.always(result)

    # log.always("Part 2:")
    # result = solve_part2(pts, start_pt, 5000 if args.test else 26501365)
    # log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
