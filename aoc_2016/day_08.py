#!/usr/bin/env python3

import sys
import traceback
from common.utils import *

try:
    import advent_of_code_ocr
except ImportError:
    advent_of_code_ocr = None


X_MAX = 50
Y_MAX = 6


def rect(points: set, x: int, y: int):
    for _x in range(x):
        for _y in range(y):
            points.add((_x, _y))


def rotate_column(points: set, col: int, n: int):
    _points = points.copy()
    points.clear()
    for x, y in _points:
        if x == col:
            y = (y + n) % Y_MAX
        points.add((x, y))


def rotate_row(points: set, col: int, n: int):
    _points = points.copy()
    points.clear()
    for x, y in _points:
        if y == col:
            x = (x + n) % X_MAX
        points.add((x, y))


def solve(lines):
    points = set()
    for line in lines:
        if line.startswith("rect "):
            _, args = line.split(" ", -1)
            x, y = map(int, args.split("x"))
            rect(points, x, y)
        elif line.startswith("rotate "):
            _, args = line.split("=", -1)
            col, n = map(int, args.split(" by "))
            if "column x" in line:
                rotate_column(points, col, n)
            else:
                rotate_row(points, col, n)
    result1 = len(points)
    image = ""
    for y in range(Y_MAX):
        for x in range(X_MAX):
            image += "#" if (x, y) in points else " "
        image += "\n"
    log.info(image)
    result2 = None
    if advent_of_code_ocr is not None:
        result2 = advent_of_code_ocr.convert_6(image.rstrip("\n"), empty_pixel=" ")
    return result1, result2


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    result1, result2 = solve(lines)

    log.always("Part 1:")
    log.always(result1)

    log.always("Part 2:")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
