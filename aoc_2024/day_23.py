#!/usr/bin/env python3
import collections
import sys
import traceback

from common.utils import *


def parse_input(args):
    nodes = set()
    links = collections.defaultdict(set)
    for line in read_lines(args.input):
        a, b = line.split("-")
        nodes.add(a)
        nodes.add(b)
        links[a].add(b)
        links[b].add(a)
    return nodes, dict(links)


def calculate_node_groups(nodes, links):
    node_groups = set()
    groups = collections.deque([(node, ) for node in nodes])
    while groups:
        group = groups.popleft()
        for node in nodes:
            if node not in group and set(group).issubset(links[node]):
                _group = tuple(sorted(group + (node, )))
                if _group not in node_groups:
                    node_groups.add(_group)
                    groups.append(_group)
    return node_groups


def solve_part1(node_groups):
    result = 0
    for node_group in node_groups:
        # print(node_group)
        if len(node_group) == 3 and any(node.startswith("t") for node in node_group):
            result += 1
    return result



def solve_part2(node_groups):
    node_group = max(node_groups, key=len)
    return ",".join(node_group)


def main():
    args = parse_args()
    nodes, links = parse_input(args)
    node_groups = calculate_node_groups(nodes, links)

    log.always("Part 1:")
    result = solve_part1(node_groups)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(node_groups)
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
