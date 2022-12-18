#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


def neighbours(pos):
    """ Calculate all cartesian neighbours of pos """
    yield pos[0] + 1, pos[1], pos[2]
    yield pos[0] - 1, pos[1], pos[2]
    yield pos[0], pos[1] + 1, pos[2]
    yield pos[0], pos[1] - 1, pos[2]
    yield pos[0], pos[1], pos[2] + 1
    yield pos[0], pos[1], pos[2] - 1


def solve_part1(data):
    """ For every position in data count connections to neighbours that are not in data """
    result = 0
    for pos in data:
        for _pos in neighbours(pos):
            if _pos not in data:
                result += 1

    return result


def solve_part2(data):
    """ Flood-fill a region surrounding data and count faces connected to data """
    def _bounds(_axis):
        """ Find bounds (+1) for axis in data """
        __vals = [__pos[_axis] for __pos in data]
        return min(__vals) - 1, max(__vals) + 1

    x_min, x_max = _bounds(0)
    y_min, y_max = _bounds(1)
    z_min, z_max = _bounds(2)
    # Start searching from a corner of the cube surrounding data, known not to be in data
    start = (x_min, y_min, z_min)
    explored = {start, }
    q = HeapQ(explored)
    result = 0
    while q:
        pos = q.pop()
        for _pos in neighbours(pos):
            if _pos in explored:
                continue
            # Skip positions that are not in bounds
            x, y, z = _pos
            if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
                if _pos in data:
                    # Neighbour is in data: this is an external face
                    result += 1
                else:
                    # Neighbour is in bounds of data but is not in data: continue searching
                    explored.add(_pos)
                    q.push(_pos)
    return result


def main():
    args = parse_args()
    data = [tuple(item) for item in read_csv_int_multiline(data_file_path_main(test=args.test), to_list=True)]

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data)
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
