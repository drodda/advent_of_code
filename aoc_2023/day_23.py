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


def parse_input(data):
    points = {}
    nodes = {}
    # Parse input, generate list of points that are path
    for y, line in enumerate(data):
        for x, sym in enumerate(line):
            point = x + y * 1j
            if sym in PATH_SYMS:
                points[point] = sym
                if y == 0 and sym == PATH_SYM:
                    nodes[LABEL_START] = point
                if y == len(data) - 1 and sym == PATH_SYM:
                    nodes[LABEL_END] = point

    # Calculate points that are network nodes: a point with 3 or more neighbours
    n_nodes = 0
    for point in sorted(points, key=lambda v: (v.imag, v.real)):
        if sum([(point + delta) in points for delta in DIRS.values()]) >= 3:
            n_nodes += 1
            label = f"{n_nodes:02d}"
            nodes[label] = point

    return points, nodes


def generate_network(points, nodes, enforce_direction=True):
    point_to_node = {v: k for k, v in nodes.items()}

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
            network[start_label][end_label] = len(path)
            continue
        deltas = NEXT_DIRS[points[point]] if enforce_direction else DIRS.values()
        for delta in deltas:
            next_point = point + delta
            if next_point not in path and next_point in points:
                queue.append((next_point, start_label, path + [point]))
    return network


def solve(network):
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
                result = max(result, _cost)
            else:
                queue.append([_cost, _path])
    return result


def main():
    args = parse_args()
    data = read_lines(input_file_path_main(test=args.test), to_list=True)
    points, nodes = parse_input(data)

    log.always("Part 1:")
    network = generate_network(points, nodes)
    result = solve(network)
    log.always(result)

    log.always("Part 2:")
    network = generate_network(points, nodes, enforce_direction=False)
    result = solve(network)
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
