#!/usr/bin/env python3

import sys
import traceback
import math

from common.utils import *


class FerryA:
    def __init__(self, dx, dy):
        self.x = 0
        self.y = 0
        self.dx = dx
        self.dy = dy

    def step(self, cmd_str):
        """ Move ferry from input """
        cmd = cmd_str[0]
        val = int(cmd_str[1:])
        if cmd in ["N", "E", "S", "W"]:
            self.move(cmd, val)
        elif cmd in ["R", "L"]:
            deg = val if cmd == "R" else (-1 * val)
            self.rotate(deg)
        elif cmd == "F":
            self.x += self.dx * val
            self.y += self.dy * val
        self.__log_always()

    def move(self, cmd, val):
        """ Move ferry (x, y) """
        if cmd == "N":
            self.y += val
        elif cmd == "E":
            self.x += val
        elif cmd == "S":
            self.y -= val
        elif cmd == "W":
            self.x -= val

    def rotate(self, deg):
        """ Rotate ferry (dx, dy) """
        rads = math.radians(deg)
        self.dx = int(math.sin(rads))
        self.dy = int(math.cos(rads))

    def get_distance(self):
        """ Calculate Manhattan distance """
        return abs(self.x) + abs(self.y)

    def __log_always(self):
        log_verbose(f"({self.__class__.__name__}: {self.x}, {self.y}), ({self.dx}, {self.dy})")


class FerryB(FerryA):

    def move(self, cmd, val):
        """ Move waypoint (dx, dy) """
        if cmd == "N":
            self.dy += val
        elif cmd == "E":
            self.dx += val
        elif cmd == "S":
            self.dy -= val
        elif cmd == "W":
            self.dx -= val

    def rotate(self, deg):
        """ Rotate waypoint (dx, dy) """
        x = self.dx
        y = self.dy
        rads = math.radians(deg)
        d_sin = int(math.sin(rads))
        d_cos = int(math.cos(rads))
        self.dx = x * d_cos + y * d_sin
        self.dy = y * d_cos - x * d_sin


def main():
    args = parse_args()

    ferry_a = FerryA(1, 0)
    ferry_b = FerryB(10, 1)

    data_file = data_file_path_main(test=args.test)
    data = read_lines(data_file, to_list=True)

    for line in data:
        log_verbose(f"{line}")
        ferry_a.step(line)
        ferry_b.step(line)

    log_always("Part 1")
    log_always(ferry_a.get_distance())
    log_always("Part 2")
    log_always(ferry_b.get_distance())


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
