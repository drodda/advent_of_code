#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from intcode_vm import *


class CartesianRobot:
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    def __init__(self, x=0, y=0, direction=UP):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self, n=1):
        self.x += self.direction[0] * n
        self.y += self.direction[1] * n

    @property
    def position(self):
        return self.x, self.y

    def rotate_left(self):
        self.direction = (self.direction[1] * -1, self.direction[0])

    def rotate_right(self):
        self.direction = (self.direction[1], self.direction[0] * -1)

    def __repr__(self):
        return f"{self.x},{self.y}"


def visualise(grid):
    """ Print grid """
    x_min = min([coord[0] for coord in grid.keys()])
    x_max = max([coord[0] for coord in grid.keys()])
    y_min = min([coord[1] for coord in grid.keys()])
    y_max = max([coord[1] for coord in grid.keys()])
    for y in range(y_max + 1, y_min - 2, -1):
        for x in range(x_min-1, x_max+2):
            print("\u25A0" if grid.get((x, y)) else " ", end="")
        print()
    print()


def run_simulation(data, start_value):
    vm = VM(data)
    robot = CartesianRobot()
    # Pre-load start_value - it will be overwritten immediately
    grid = {robot.position: start_value}
    try:
        i = 0
        while True:
            i += 1
            vm.input.put(grid.get(robot.position, 0))
            color = vm.run_until_output()
            direction = vm.run_until_output()
            log.info(f"{i}: At {robot.position} facing {robot.direction}, color {grid.get(robot.position, 0)}, painting {color}, direction {direction}")
            grid[robot.position] = color
            if direction == 0:
                robot.rotate_left()
            elif direction == 1:
                robot.rotate_right()
            else:
                raise RuntimeError(f"Invalid direction: {direction}")
            robot.move()
    except StopIteration:
        pass
    return grid


def main():
    parse_args()
    data = read_csv_int(data_file_path_main(test=False), to_list=True)

    log.always("Part 1")
    log.always(len(run_simulation(data, 0)))

    log.always("Part 2")
    grid = run_simulation(data, 1)
    visualise(grid)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
