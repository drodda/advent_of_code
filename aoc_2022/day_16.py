#!/usr/bin/env python3

import functools
import re
import sys
import traceback
from common.utils import *


def parse_input(input_path):
    _re = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
    lines = read_lines(input_path)
    flow_rates = {}
    connections = {}
    for line in lines:
        pos, flow_rate_str, connections_str = _re.match(line).groups()
        flow_rate = int(flow_rate_str)
        if flow_rate > 0:
            flow_rates[pos] = flow_rate
        connections[pos] = connections_str.split(", ")
    return flow_rates, connections


def calculate_path_len(connections, start, end):
    path_len = 1
    path_heads = connections[start]
    while path_heads:
        next_path_heads = set()
        for node in path_heads:
            if node == end:
                return path_len
            next_path_heads = next_path_heads.union(connections[node])
        path_heads = next_path_heads
        path_len += 1
    return None


def solve(flow_rates, paths, t_max=30, do_part_2=False):
    @functools.lru_cache(maxsize=None)
    def _solve(position, t, opened, move_elephant=False):
        if t > 15 and not move_elephant:
            log.info(f"Searching: {t} ('human') {position} {opened}")
        else:
            log.debug(f"Searching: {t} ({'elephant' if move_elephant else 'human'}) {position} {opened}")
        if t < 0 or len(opened) == len(flow_rates):
            return 0
        result = 0
        # Try to move the human
        for _position, _cost in paths[position].items():
            _t = t - _cost - 1
            if _position not in opened and _t > 0:
                # Move to _position and open valve
                _opened = tuple(sorted(opened + (_position, )))
                _result = flow_rates[_position] * _t
                _result += _solve(_position, _t, _opened, move_elephant=move_elephant)
                result = max(result, _result)
        # Also end the human's movement, move elephant
        if do_part_2 and not move_elephant and position != "AA":
            _result = _solve("AA", t_max, opened, move_elephant=True)
            result = max(result, _result)
        return result
    return _solve("AA", t_max, tuple())


def main():
    args = parse_args()
    flow_rates, connections = parse_input(args.input)

    # Calculate paths between all nodes with non-zero flow rate
    paths = {}
    for start in ["AA", *flow_rates.keys()]:
        paths[start] = {}
        for end in flow_rates.keys():
            if end != start:
                paths[start][end] = calculate_path_len(connections, start, end)

    log.always("Part 1:")
    result = solve(flow_rates, paths, t_max=30)
    log.always(result)

    log.always("Part 2:")
    result = solve(flow_rates, paths, t_max=26, do_part_2=True)
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
