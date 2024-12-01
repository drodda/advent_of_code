#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


def parse(lines):
    network = collections.defaultdict(set)
    for line in lines:
        a_node, nodes = line.split(": ")
        for b_node in nodes.split(" "):
            network[a_node].add(b_node)
            network[b_node].add(a_node)
    return dict(network)


def node_connections_to_subset(network, subset, node):
    """ Calculate the number of direct connections between node and nodes in subset """
    return len(network[node].intersection(subset))


def connections_to_subset(network, subset):
    """ Calculate the number of connections between nodes in subset and nodes not in subset """
    return sum(node_connections_to_subset(network, subset, node) for node in network if node not in subset)


def solve(network):
    log.info(network)

    subset = set()
    while connections_to_subset(network, subset) != 3:
        log.info(f"{subset} = {connections_to_subset(network, subset)}")
        # Move the node with most connections to the subset
        # Initially this will be a random node
        move_node = None
        max_connections = -1
        for node in network:
            if node not in subset:
                n_connections = node_connections_to_subset(network, subset, node)
                if n_connections > max_connections:
                    max_connections = n_connections
                    move_node = node
        log.info(f"Removing node: {move_node}")
        subset.add(move_node)

    log.info(f"subset: {subset}")
    return len(subset) * (len(network) - len(subset))


def main():
    args = parse_args()
    lines = read_lines(args.input, to_list=True)
    network = parse(lines)

    log.always("Part 1:")
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
