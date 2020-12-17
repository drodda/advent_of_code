#!/usr/bin/env python3
import traceback
import itertools

from utils import *


N_CYCLES = 6


def parse_input(lines):
    result = []
    # x_min =
    z = 0
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c == "#":
                result.append((x, y, z, 0))
    return result


def get_limit(data, axis):
    col_min = min([row[axis] for row in data])
    col_max = max([row[axis] for row in data])
    return col_min, col_max


def get_range(data, axis):
    return sorted(list(set([row[axis] for row in data])))


# def get_range_with_offset(data, axis, offset):
#     values = get_range(data, axis)
#     offsets = list(range(0-offset, offset+2))
#     result = sorted(list(set((a+b) for a, b in itertools.product(values, offsets))))
#     return result


def generate_neighbours(x, y, z, w, remove_self=True):
    neighbours = set(itertools.product(range(x-1, x+2), range(y-1, y+2), range(z-1, z+2), range(w-1, w+2)))
    if remove_self:
        neighbours.remove((x, y, z, w))
    return neighbours


def step_element(state, occupied_neighbours):
    return (state and 2 <= occupied_neighbours <= 3) or (not state and occupied_neighbours == 3)


def step_simulation(data):
    x_min, x_max = get_limit(data, 0)
    y_min, y_max = get_limit(data, 1)
    z_min, z_max = get_limit(data, 2)
    w_min, w_max = get_limit(data, 3)

    x_range = range(x_min - 1, x_max + 2)
    y_range = range(y_min - 1, y_max + 2)
    z_range = range(z_min - 1, z_max + 2)
    w_range = range(w_min - 1, w_max + 2)
    # x_range = get_range_with_offset(data, 0, 1)
    # y_range = get_range_with_offset(data, 1, 1)
    # z_range = get_range_with_offset(data, 2, 1)
    # w_range = get_range_with_offset(data, 3, 1)

    result = []
    for x in x_range:
        for y in y_range:
            for z in z_range:
                for w in w_range:
                    occupied_neighbours = sum([neighbour in data for neighbour in generate_neighbours(x, y, z, w)])
                    if step_element((x, y, z, w) in data, occupied_neighbours):
                        result.append((x, y, z, w))
    return result


def coord_to_char(data, x, y, z, w):
    return "#" if (x, y, z, w) in data else "."


def print_data(data):
    x_min, x_max = get_limit(data, 0)
    y_min, y_max = get_limit(data, 1)
    z_min, z_max = get_limit(data, 2)
    w_min, w_max = get_limit(data, 3)
    for w in range(w_min, w_max + 1):
        for z in range(z_min, z_max+1):
            print(f"Z = {z}, W = {w}:")
            for x in range(x_min, x_max + 1):
                row = [coord_to_char(data, x, y, z, w) for y in range(y_min, y_max+1)]
                print("".join(row))
            print()


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    lines = read_lines(data_file)
    data = parse_input(lines)
    if args.verbose:
        print_data(data)

    for i in range(N_CYCLES):
        data = step_simulation(data)
        if args.debug:
            x_min, x_max = get_limit(data, 0)
            y_min, y_max = get_limit(data, 1)
            z_min, z_max = get_limit(data, 2)
            w_min, w_max = get_limit(data, 3)
            print("######################################")
            print(f"Step {i+1}: {x_max-x_min} * {y_max-y_min} * {z_max-z_min} * {w_max-w_min}")
            if args.verbose:
                print_data(data)
    print(len(data))

    # print("Part 1")
    # print("Part 2")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
