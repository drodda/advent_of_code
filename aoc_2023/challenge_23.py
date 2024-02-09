#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


DIRS = {
    "^": -1j,
    ">": 1+0j,
    "v": 1j,
    "<": -1+0j,
}

PATH_SYM = "."

NEXT_DIRS = {
    **{
        sym: [delta] for sym, delta in DIRS.items()
    },
    PATH_SYM: list(DIRS.values()),
}

PATH_SYMS = list(NEXT_DIRS.keys())

LABEL_START = "START"
LABEL_END = "END"


def parse(data):
    points = {}
    nodes = {}
    start = None
    end = None
    # Parse input, generate list of points that are path
    for y, line in enumerate(data):
        for x, sym in enumerate(line):
            point = x + y * 1j
            if sym in PATH_SYMS:
                points[point] = sym
                if y == 0 and sym == PATH_SYM:
                    log.debug(f"Node: {LABEL_START} = {point}")
                    nodes[LABEL_START] = point
                if y == len(data) - 1 and sym == PATH_SYM:
                    log.debug(f"Node: {LABEL_END} = {point}")
                    nodes[LABEL_END] = point

    # Calculate points that are network nodes
    n_nodes = 0
    for point in sorted(points, key=lambda v: (v.imag, v.real)):
        if sum([(point + delta) in points for delta in DIRS.values()]) >= 3:
            n_nodes += 1
            label = f"{n_nodes:02d}"
            log.debug(f"Node: {label} = {point}")
            nodes[label] = point
    point_to_node = {v: k for k, v in nodes.items()}

    # Calculate network
    network = {label: {} for label in nodes.keys()}
    queue = collections.deque()
    for label, start_point in nodes.items():
        for delta in DIRS.values():
            next_point = start_point + delta
            if next_point in points:
                queue.append((next_point, label, [start_point, ]))
    while queue:
        point, start_label, path = queue.popleft()
        if point in point_to_node:
            end_label = point_to_node[point]
            log.debug(f"Connection: {start_label} {(nodes[start_label])} - {end_label} ({nodes[end_label]}) = {len(path)}")
            network[start_label][end_label] = len(path)
            continue
        for delta in NEXT_DIRS[points[point]]:
            next_point = point + delta
            if next_point not in path and next_point in points:
                queue.append((next_point, start_label, path + [point]))
    log.info(network)
    return network


def solve_part1(network):
    result = 0

    queue = collections.deque([[0, [LABEL_START]]])
    while queue:
        cost, path = queue.popleft()
        for node, path_cost in network[path[-1]].items():
            if node in path:
                continue
            _cost = cost + path_cost
            _path = path + [node]
            if node == LABEL_END:
                log.info(f"Path {_path} cost {_cost}")
                result = max(result, _cost)
            else:
                queue.append([_cost, _path])
    return result


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)
    network = parse(data)

    log.always("Part 1:")
    result = solve_part1(network)
    log.always(result)

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
