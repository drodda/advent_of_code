#!/usr/bin/env python3

import collections
import re
import sys
import traceback

from common.utils import *


def parse_input(lines):
    result = collections.defaultdict(dict)
    for line in lines:
        m = re.match(r"(?P<dest1>\S+) to (?P<dest2>\S+) = (?P<dist>\d+)", line)
        if m:
            dest1, dest2, dist = m.groups()
            dist = int(dist)
            result[dest1][dest2] = dist
            result[dest2][dest1] = dist
        else:
            log_error(f"Bad line: {line}")
    return result


def all_paths(connections):
    """ # Dijkstra find all path that covers all nodes defined by connections, yield shortest first """
    all_destinations = set(connections.keys())
    explored = set()
    path_heads = HeapQ()  # queue: [cost, path]
    # Pre-populate queue with all nodes as possible starting pointss
    for node in all_destinations:
        path_heads.push((0, (node, )))

    while path_heads:
        cost, path = path_heads.pop()
        if set(path) == all_destinations:
            log_verbose(f"Solution found: {path} cost {cost}")
            yield cost, path
        if path in explored:
            continue
        explored.add(path)
        log_verbose(f"Searching: {path} cost {cost}")
        node = path[-1]
        # Explore all connections from node
        for _node, _cost in connections[node].items():
            if _node not in path:
                path_heads.push((cost + _cost, path + (_node, )))


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    connections = parse_input(lines)

    paths = all_paths(connections)

    log_always("Part 1")
    cost, path = next(paths)
    log_always(cost)

    log_always("Part 2")
    # Drain paths, keep last
    *_, (cost, path) = paths
    log_always(cost)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
