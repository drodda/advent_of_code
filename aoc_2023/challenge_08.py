#!/usr/bin/env python3
import math
import sys
import traceback
from common.utils import *


DIRECTION_INDEX = {
    "L": 0,
    "R": 1,
}


def parse_input(_input):
    directions = next(_input)[0]
    lines = next(_input)
    node_map = {}
    for line in lines:
        start, dests_str = line.split(" = ", 1)
        dests = dests_str.strip("()").split(", ", 1)
        node_map[start] = dests
    return directions, node_map


def solve(directions, node_map, node, end_condition):
    i = 0
    while not node.endswith(end_condition) or i == 0:
        _dir = directions[i % len(directions)]
        i += 1
        node = node_map[node][DIRECTION_INDEX[_dir]]
        log.debug(f"  {node}: {end_condition} = {node.endswith(end_condition)}")
    return i, node


def solve_part2(directions, node_map):
    start_nodes = [node for node in node_map.keys() if node.endswith("A")]
    steps_to_end = []
    for node in start_nodes:
        steps, end_node = solve(directions, node_map, node, "Z")
        steps_repeat, _ = solve(directions, node_map, end_node, end_node)
        if steps != steps_repeat:
            log.error(f"Error: Node {node} -> {end_node} does not loop as expected")
        log.debug(f"{node} completes in {steps}, repeats after {steps_repeat}")
        steps_to_end.append(steps)
    return math.lcm(*steps_to_end)


def main():
    args = parse_args()
    _input = read_multilines(data_file_path_main(test=args.test))
    directions, node_map = parse_input(_input)

    if not args.test:
        log.always("Part 1:")
        result, _ = solve(directions, node_map, "AAA", "ZZZ")
        log.always(result)

    log.always("Part 2:")
    result = solve_part2(directions, node_map)
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
