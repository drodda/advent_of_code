#!/usr/bin/env python3

import collections
import sys
import traceback
import string
import numpy as np

from common.utils import *


START = "AA"
END = "ZZ"


def find_portals(world):
    """ Search entire world for portals.
        Inefficient, as most of the world can not be portal, but must simpler than targeted search of outer and inner edge
    """
    start = None
    end = None
    portals = {}
    tmp_portals = {}  # Store location of portals until the other end is found
    for y in range(2, len(world) - 2):
        for x in range(2, len(world[y]) - 2):
            pos = (y, x)
            neighbours = [
                ((y - 2, x), (y - 1, x)),
                ((y, x + 1), (y, x + 2)),
                ((y + 1, x), (y + 2, x)),
                ((y, x - 2), (y, x - 1)),
            ]
            if world[pos] == ".":
                # for n0, n1 in dual_neighbours(pos):
                for n0, n1 in neighbours:
                    if world[n0] in string.ascii_letters and world[n1] in string.ascii_letters:
                        portal_name = world[n0] + world[n1]
                        if portal_name == START:
                            start = pos
                            portals[pos] = (None, 0, portal_name)
                        elif portal_name == END:
                            end = pos
                            portals[pos] = (None, 0, portal_name)
                        elif portal_name in tmp_portals:
                            # Far end of the portal is known
                            # Assume if this portal is on the outer edge, the other end must be inner edge
                            is_outer = (x <= 2) or (x >= len(world[y]) - 3) or (y <= 2) or (y >= len(world) - 3)
                            direction = -1 if is_outer else 1
                            _pos = tmp_portals.pop(portal_name)
                            portals[pos] = (_pos, direction, portal_name)
                            portals[_pos] = (pos, -direction, portal_name)
                        else:
                            # Far end of the portal has not yet been found. Save it for later
                            tmp_portals[portal_name] = pos

    return start, end, portals


def find_paths(world, start_pos, destinations):
    """ Find the shortest path from start_pos any other destination that can be reached directly """
    path_heads = collections.deque([(0, start_pos)])
    explored = {start_pos, }
    result = []
    while path_heads:
        cost, pos = path_heads.popleft()
        neighbours = [
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
        ]
        _cost = cost + 1
        for _pos in neighbours:
            if _pos not in explored and world[_pos] == ".":
                explored.add(_pos)
                if _pos in destinations:
                    result.append((_pos, _cost))
                path_heads.append((_cost, _pos))
    return result


def solve(start, end, portals, paths, recursive_spaces=False):
    # Dijkstra find shortest path between start and end
    explored = set()
    path_heads = HeapQ([(0, 0, start, f"{START}:0")])

    while path_heads:
        cost, level, pos, path_str = path_heads.pop()
        _, _, portal_name = portals[pos]
        if (pos, level) in explored:
            continue
        log_debug(f"Searching {pos} {portal_name} level {level} cost {cost} via {path_str}")
        if pos == end and level == 0:
            log_info(f"Result: {pos}: {portal_name} {path_str} = {cost}")
            return cost
        explored.add((pos, level))

        if pos != start and pos != end:
            # Search far end of portal
            _pos, _direction, _portal_name = portals[pos]
            _level = level + (_direction if recursive_spaces else 0)
            if _level >= 0:
                _path_str = f"{path_str}->{_portal_name}:{_level}"
                path_heads.push((cost + 1, _level, _pos, _path_str))
        # Search all locations that can be reached from pos
        for _pos, _cost in paths[pos]:
            path_heads.push((cost + _cost, level, _pos, path_str))
    return


def print_world(world):
    for y in range(len(world)):
        log_debug("".join(world[y]))
    log_debug("")


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)

    world = np.array([[c for c in s] for s in data])
    print_world(world)

    # Find all portals
    start, end, portals = find_portals(world)

    # Find paths from each destination to all other destinations
    paths = {pos: find_paths(world, pos, portals.keys()) for pos in portals.keys()}

    log_always("Part 1")
    result = solve(start, end, portals, paths)
    log_always(result)
    log_always("")

    log_always("Part 2")
    result = solve(start, end, portals, paths, recursive_spaces=True)
    log_always(result)
    log_always("")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
