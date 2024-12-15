#!/usr/bin/env python3
import collections
import re
import sys
import traceback

import png

from common.utils import *


RE_INPUT = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
SIZE = (101, 103)
SIZE_TEST = (11, 7)



def parse_input(args):
    positions = []
    velocities = []
    for line in read_lines(args.input):
        p_x, p_y, v_x, v_y = map(int, re.fullmatch(RE_INPUT, line).groups())
        positions.append((p_x, p_y))
        velocities.append((v_x, v_y))
    return positions, velocities


def move(pos, vel, size):
    return (pos[0] + vel[0]) % size[0], (pos[1] + vel[1]) % size[1]


def quadrant(pos, size):
    x, y = pos
    median_x = (size[0] - 1) / 2
    median_y = (size[1] - 1) / 2
    if x == median_x or y == median_y:
        return None
    return ("N" if y < median_y else "S") + ("W" if x < median_x else "E")


def solve_part1(positions, velocities, size):
    for i in range(100):
        positions = [move(pos, vel, size) for pos, vel in zip(positions, velocities)]

    quadrants = [quadrant(pos, size) for pos in positions]
    quadrant_counts = collections.Counter(quadrants)
    result = 1
    for _quadrant, count in quadrant_counts.items():
        if _quadrant is not None:
            result *= count
    return result


WHITE = 255
BLACK = 0


def write_image(output_path, positions, size):
    img = []
    for y in range(size[1]):
        row = [(WHITE if (x, y) in positions else BLACK) for x in range(size[0])]
        img.append(row)
    writer = png.Writer(size[0], size[1], greyscale=True)
    with open(output_path, "wb") as f:
        writer.write(f, img)


def solve_part2(positions, velocities, size, test=False):
    # Loop until no points overlay, this happens to be the end solution?
    result = 0
    while True:
        positions = [move(pos, vel, size) for pos, vel in zip(positions, velocities)]
        result += 1
        if len(set(positions)) == len(positions):
            break
    output_path = "day_14_test.png" if test else "day_14.png"
    write_image(output_path, positions, size)

    return result


def main():
    args = parse_args()
    positions, velocities = parse_input(args)
    size = SIZE_TEST if args.test else SIZE

    log.always("Part 1:")
    result = solve_part1(positions, velocities, size)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(positions, velocities, size, test=args.test)
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
