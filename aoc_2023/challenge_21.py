#!/usr/bin/env python3

import sys
import traceback
from common.utils import *


DIRS = {
    "N": -1j,
    "E": 1+0j,
    "S": 1j,
    "W": -1+0j,
}


def parse(data):
    pts = set()
    start = None
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            pos = x + y * 1j
            if c in [".", "S"]:
                pts.add(pos)
                if c == "S":
                    start = pos
    return start, pts


def mod_real(v, modulo):
    return (v.real % modulo) + (v.imag % modulo) * 1j


def simulate(pts, start, n_steps):
    grid_size = int(max(pt.real for pt in pts)) + 1
    points = start
    for i in range(n_steps):
        _n_points = set()
        for pt in points:
            for delta in DIRS.values():
                _pt = pt + delta
                if mod_real(_pt, grid_size) in pts:
                    _n_points.add(_pt)
        points = _n_points
        log.debug(f"{i}: {len(points)}")
    return points


def solve_part2(pts, start_pt, n_steps):
    grid_size = int(max(pt.real for pt in pts)) + 1

    # The number of occupied spaces tends towards a quadratic when measured at the scale of the grid size
    # Calculate number of occupied spaces at grid size intervals

    start_steps = n_steps % grid_size
    points = simulate(pts, {start_pt, }, start_steps)
    y0 = len(points)
    log.info(f"{start_steps} = {y0}")

    points = simulate(pts, points, grid_size)
    y1 = len(points)
    log.info(f"{start_steps + grid_size} = {y1}")

    points = simulate(pts, points, grid_size)
    y2 = len(points)
    log.info(f"{start_steps + 2 * grid_size} = {y2}")

    # Calculate quadratic coefficients
    c = y0
    b = (4 * y1 - y2 - 3 * c) / 2
    a = y1 - b - c

    # Use quadratic
    x = (n_steps - start_steps) // grid_size
    return int(a * x ** 2 + b * x + c)


def main():
    args = parse_args()
    data = read_lines(data_file_path_main(test=args.test), to_list=True)
    start_pt, pts = parse(data)

    log.always("Part 1:")
    result = len(simulate(pts, {start_pt, }, 6 if args.test else 64))
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(pts, start_pt, 5000 if args.test else 26501365)
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
