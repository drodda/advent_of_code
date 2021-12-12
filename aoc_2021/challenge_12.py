#!/usr/bin/env python3

import os
import sys
import traceback
from collections import defaultdict

from utils import *


def find_paths(node_map, path=None, extra_stops=0):
    """ Find all possible paths from 'start' to 'end' using node connections node_map
        Large nodes (capital letters) can be visited more than once.
        Small nodes (lowercase letters) can be visited only once ...
            (part 2) except for at most extra_stops re-visits to a small node
    """
    if path is None:
        path = ["start"]
    node = path[-1]
    # For all connected nodes
    for _node in node_map[node]:
        _path = path + [_node]
        if _node == "end":
            yield _path
        # Never return to start
        elif _node == "start":
            continue
        # Filter out nodes that should not be revisited
        elif not _node.islower() or _node not in path:
            yield from find_paths(node_map, _path, extra_stops)
        # Part 2: Allow up to extra_stops visits to small nodes
        elif extra_stops > 0:
            yield from find_paths(node_map, _path, extra_stops - 1)


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))
    node_map = defaultdict(set)
    for line in lines:
        node_a, node_b = line.split("-")
        node_map[node_a].add(node_b)
        node_map[node_b].add(node_a)
    log_verbose(node_map)

    log_always("Part 1:")
    paths = list(find_paths(node_map))
    log_always(len(paths))

    log_always("Part 2:")
    paths = list(find_paths(node_map, extra_stops=1))
    log_always(len(paths))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
