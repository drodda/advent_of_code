#!/usr/bin/env python3

import sys
import copy
import traceback

from common.utils import *


SYM_O = "#"   # Occupied
SYM_U = "L"   # Unoccupied
SYM_P = " "   # Pad
SYM_F = "."   # Floor
SYM_UNK = "?" # Unknown?


DIRECTIONS = (
    # Queens-move directions in cartesian coordinates
    (1, 0),    # N
    (1, 1),    # NE
    (0, 1),    # E
    (-1, 1),   # SE
    (-1, 0),   # S
    (-1, -1),  # SW
    (0, -1),   # W
    (1, -1),   # NW
)


def pad_data(data, pad=SYM_P):
    """ Pad data with pad symbol. Data must be a 2D array of arrays of characters
        For a m * n 2D array of characters, return a (m+2) * (n+2) array
    """
    row_len = len(data[0])
    row_empty = list(pad * (row_len + 2))
    data_pad = [row_empty] + [[pad] + row + [pad] for row in data] + [row_empty]
    return data_pad


def debug_print_data(data, indent="> "):
    for row in data:
        log.debug(indent + "".join(row))


def get_neighbours(data, i, j):
    """ Return a list of 8 neighbouring cells around data[i][j]
        Unsafe: i and j must not be on the edge of data
    """
    return data[i-1][(j-1):(j+2)] + [data[i][j-1], data[i][j+1]] + data[i+1][(j-1):(j+2)]


def get_visible(data, i, j, ignore=(SYM_F,)):
    """ Return a list of nearest neighbour in each direction ignoring values in ignore list
        Unsafe: i and j must not be on the edge of data, and there must be a non-ignored element in each direction
    """
    return [get_visible_direction(data, i, j, di, dj, ignore) for di, dj in DIRECTIONS]


def get_visible_direction(data, i, j, di, dj, ignore):
    """ Return the nearest element from (i, j) in direction (di, dj) that is nto in ignore list
        Unsafe: i and j must not be on the edge of data, and there must be a non-ignored element in direction (di, dj)
    """
    while True:
        i = i + di
        j = j + dj
        if data[i][j] not in ignore:
            # Return the first non-floor element found
            return data[i][j]


def count_seats(data, value):
    """ Count the number of items in data that are value """
    result = 0
    for row in data:
        result += sum(x == value for x in row)
    return result


def mutate(data, neighbour_func, occupied_thresh):
    """ Mutate data. Use neighbour_func to calculate the number of occupied neighbouring seats,
         and occupied_thresh to determine if an occupied seat should be unoccupied
        Returns new data state and boolean on whether the data has changed
    """
    result = copy.deepcopy(data)
    for i in range(1, len(data)-1):
        for j in range(1, len(data[0])-1):
            if data[i][j] in [SYM_U, SYM_O]:
                neighbours = neighbour_func(data, i, j)
                occupied_neighbours = neighbours.count(SYM_O)
                if data[i][j] == SYM_U and occupied_neighbours == 0:
                    result[i][j] = SYM_O
                elif data[i][j] == SYM_O and occupied_neighbours >= occupied_thresh:
                    result[i][j] = SYM_U
    return result, (result == data)


def mutate_until_stable(data, neighbour_func, occupied_thresh):
    """ Mutate data using neighbour_func and occupied_thresh until data does not change.
        Returns the final arrangement and number of iterations
    """
    i = 0
    while True:
        data, changed = mutate(data, neighbour_func, occupied_thresh)
        if changed:
            break
        i += 1
        log.debug()
        log.debug(i)
        debug_print_data(data)

    return data, i


def main():
    args = parse_args()

    data_file = args.input
    data_orig = read_lines(data_file)
    data_orig = [list(line) for line in data_orig]
    data = pad_data(data_orig)

    debug_print_data(data)

    log.always("Part 1")
    data_final, i = mutate_until_stable(data, get_neighbours, 4)
    log.always(count_seats(data_final, SYM_O))

    log.always("Part 2")
    data_final, i = mutate_until_stable(data, get_visible, 5)
    log.always(count_seats(data_final, SYM_O))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
