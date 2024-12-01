#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def parse_data(data_raw):
    result = []
    for y, line in enumerate(data_raw):
        for x, c in enumerate(line):
            if c == "#":
                result.append((x, y))
    return result


def debug_print_data(nodes, node=None):
    x_max = max([x for x, y in nodes])
    y_max = max([y for x, y in nodes])
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            print("O" if (x, y) == node else "#" if (x, y) in nodes else ".", end="")
        print()
    print()


def is_between(pt1, pt2, check):
    """ Return True if check is between pt1 and pt2 """
    x1, y1 = pt1
    x2, y2 = pt2
    xc, yc = check
    if xc < min(x1, x2) or xc > max(x1, x2) or yc < min(y1, y2) or yc > max(y1, y2):
        return False
    # Calculate cross product between (pt1 - check) and (pt2 - check):
    cross_product = (xc - x1) * (yc - y2) - (xc - x2) * (yc - y1)
    return cross_product == 0


def distance(pt1, pt2):

    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


def direction(pt1, pt2, decimals=8):
    """ Semi-polar direction: Up (negative-y) is zero, clockwise is positive """
    return np.round(
        np.mod(
            np.arctan2((pt2[0] - pt1[0]), (pt1[1] - pt2[1])),
            2 * np.pi
        ), decimals
    )


def to_polar(pt1, pt2):
    """ Return polar coordinates (distance, direction) between pt1 and pt2 """
    return distance(pt1, pt2), direction(pt1, pt2)


def node_see_count(nodes, node):
    """ Return the number of nodes seen by node """
    directions = [direction(node, pt) for pt in nodes if pt != node]
    return np.unique(directions).size


def calculate_part_1(nodes):
    node_best = None
    node_best_count = 0
    for node in nodes:
        node_count = node_see_count(nodes, node)
        if node_count > node_best_count:
            node_best = node
            node_best_count = node_count
    return node_best, node_best_count


def calculate_part_2(nodes, node):
    # Calculate (semi-)polar coordinates between node and all other nodes in data
    nodes_distance = {pt: distance(node, pt) for pt in nodes if pt != node}
    nodes_direction = {pt: direction(node, pt) for pt in nodes if pt != node}
    directions = np.unique([v for v in nodes_direction.values()])
    # Group nodes by direction, in order of distance
    nodes_by_direction = []
    for _direction in directions:
        nodes_by_direction.append(
            sorted(
                [pt for pt in nodes if pt != node and nodes_direction[pt] == _direction],
                key=nodes_distance.get,
                reverse=True,
            )
        )
    # Start eliminating
    result = None
    i = 0
    while nodes_by_direction:
        for _nodes_list in nodes_by_direction:
            i += 1
            node_destroyed = _nodes_list.pop()
            log.verbose(f"{i}: {node_destroyed}\t{nodes_direction[node_destroyed]}")
            if i == 200:
                result = node_destroyed[0] * 100 + node_destroyed[1]
        # Trim empty directions
        nodes_by_direction = [_nodes_list for _nodes_list in nodes_by_direction if _nodes_list]
    return result


def main():
    args = parse_args()
    nodes = parse_data(read_lines(args.input))
    log.always("Part 1:")
    node, count = calculate_part_1(nodes)
    log.info(f"Best node: {node}")
    if args.verbose:
        print()
        debug_print_data(nodes, node)
    log.always(count)
    log.always("Part 2:")
    result = calculate_part_2(nodes, node)
    print(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
