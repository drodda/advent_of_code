#!/usr/bin/env python3

import json
import sys
import traceback
import collections

from utils import *


def parse_input(lines):
    # Set of all nodes
    nodes = set()
    # node to orbiting nodes dict
    node_children = collections.defaultdict(list)
    # node to parent dict
    nodes_parent = {}

    for line in lines:
        # b orbits a
        a, b = line.split(")")
        nodes.add(a)
        nodes.add(b)
        node_children[a].append(b)
        nodes_parent[b] = a

    # Map of all child nodes
    node_map = node_dict_to_map(node_children, "COM")

    return nodes, node_children, nodes_parent, node_map


def node_dict_to_map(nodes_dict, node):
    """ Return a dictionary of child elements of node,
         with value a recursive dictionary of child elements of each element
     """
    result = {}
    if node in nodes_dict:
        for item in nodes_dict.get(node, []):
            result[item] = node_dict_to_map(nodes_dict, item)
    return result


def calculate_checksum(node_map):
    """ Calculate the checksum of node_map (Challenge Part 1) """
    result = count_children(node_map)
    for child, child_node_map in node_map.items():
        result += calculate_checksum(child_node_map)
    return result


def count_children(node_map):
    """ Count the number of nodes in node_map """
    result = 0
    for child, child_node_map in node_map.items():
        result += 1 + count_children(child_node_map)
    return result


def node_parents_list(node, nodes_parent):
    """ Return a list of the parent of node, parnet of parnet of node, ... """
    result = []
    while node in nodes_parent:
        parent = nodes_parent[node]
        result.append(parent)
        node = parent
    return result


def path_between(node_a, node_b, nodes_parent):
    """ Calculate the path between node_a and node_b using each node's parent """
    path_a = node_parents_list(node_a, nodes_parent)
    path_b = node_parents_list(node_b, nodes_parent)
    if path_a[-1] != path_b[-1]:
        return None
    common_node = path_a[-1]
    while path_a and path_b and path_a[-1] == path_b[-1]:
        common_node = path_a[-1]
        path_a.pop()
        path_b.pop()
    # Reverse path_b as it will be traversed backwards
    path_b.reverse()
    result = path_a + [common_node] + path_b
    return result


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test))
    nodes, node_children, nodes_parent, node_map = parse_input(data)

    log_verbose(json.dumps(node_map, indent=2))

    log_always("Part 1")
    log_always(calculate_checksum(node_map))

    if args.test:
        data = read_lines(data_file_path("test", "b"))
        nodes, node_children, nodes_parent, node_map = parse_input(data)

    log_always("Part 2")
    path_you_san = path_between("YOU", "SAN", nodes_parent)
    log_verbose(path_you_san)
    # Number of transfers is path length - 1 as YOU is already a child of path[0]
    log_always(len(path_you_san) - 1)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
