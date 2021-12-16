#!/usr/bin/env python3
import os
import queue
import time
import traceback

from utils import *
from intcode_vm import *


DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3
DIRECTION_EAST = 4

DIRECTIONS_CW = {
    DIRECTION_NORTH: DIRECTION_EAST,
    DIRECTION_EAST: DIRECTION_SOUTH,
    DIRECTION_SOUTH: DIRECTION_WEST,
    DIRECTION_WEST: DIRECTION_NORTH,
}

DIRECTIONS_CCW = {
    DIRECTION_NORTH: DIRECTION_WEST,
    DIRECTION_WEST: DIRECTION_SOUTH,
    DIRECTION_SOUTH: DIRECTION_EAST,
    DIRECTION_EAST: DIRECTION_NORTH,
}

EVENT_NO_MOVE = 0
EVENT_MOVED = 1
EVENT_MOVED_OXYGEN = 2


SPACE_VOID = 0
SPACE_WALL = 1
SPACE_OXYGEN = 2


def position_move(position, direction):
    x, y = position
    y += 1 if direction == DIRECTION_NORTH else -1 if direction == DIRECTION_SOUTH else 0
    x += 1 if direction == DIRECTION_EAST else -1 if direction == DIRECTION_WEST else 0
    return x, y


def bounds(world):
    """ Return bounds for world dictionary """
    x_min = min([x for x, y in world.keys()])
    x_max = max([x for x, y in world.keys()])
    y_min = min([y for x, y in world.keys()])
    y_max = max([y for x, y in world.keys()])
    return x_min, y_min, x_max, y_max


def visualise(world, position):
    x_min, y_min, x_max, y_max = bounds(world)
    symbols = {
        SPACE_VOID: ".",
        SPACE_WALL: "#",
        SPACE_OXYGEN: "O",
        None: " ",
    }
    print("================")
    for y in range(y_max, y_min - 1, -1):
        for x in range(x_min, x_max + 1):
            print("D" if (x, y) == position else symbols[world.get((x, y))], end="")
        print()
    print("================")



def robot_move(vm, world, position, direction):
    time.sleep(1)
    visualise(world, position)
    print("running ...")
    vm.run_until_input()
    print(f"Input requested - {direction}")
    vm.input.put(direction)
    print("running ...")
    event = vm.run_until_output()
    print(f"Got output: {event}")
    _position = position_move(position, direction)
    moved = False
    oxygen_found = False
    if event == EVENT_MOVED:
        position = _position
        world[position] = SPACE_VOID
        moved = True
    elif event == EVENT_MOVED_OXYGEN:
        position = _position
        world[position] = SPACE_OXYGEN
        moved = True
        oxygen_found = True
    elif event == EVENT_NO_MOVE:
        world[_position] = SPACE_WALL
        # Change direction
    else:
        raise RuntimeError("Invalid output?")
    return position, moved, oxygen_found


def robot_search(vm, world, position, direction):
    """ returns: position, oxygen_found, reverse_direction """
    direction_ccw = DIRECTIONS_CCW[direction]
    while True:
        # First try to move the CCW direction. If robot can move, return reverse_direction
        position, moved, oxygen_found = robot_move(vm, world, position, direction_ccw)
        if oxygen_found or moved:
            return position, True, oxygen_found
        # Next try to move the desired direction. If robot can't move, return
        position, moved, oxygen_found = robot_move(vm, world, position, direction)
        if oxygen_found or not moved:
            return position, False, oxygen_found


def find_oxygen(data):
    vm = VM(data)
    position = (0, 0)
    world = {position: SPACE_VOID}

    # Move North until a wall is found
    while True:
        position, moved, oxygen_found = robot_move(vm, world, position, DIRECTION_NORTH)
        if oxygen_found:
            return position
        if not moved:
            break
    # Move east and south
    for direction in [DIRECTION_EAST, DIRECTION_SOUTH]:
        while True:
            position, moved, oxygen_found = robot_move(vm, world, position)
            if oxygen_found:
                return position
            if not moved:
                break


    while True:
        for direction in [DIRECTION_NORTH, DIRECTION_EAST, DIRECTION_SOUTH, DIRECTION_WEST]:
            while True:
                vm.run_until_input()
                print(f"Input requested - {direction}")
                vm.input.put(direction)
                print("running ...")
                event = vm.run_until_output()
                print(f"Got output: {event}")
                _position = position_move(position, direction)
                if event == EVENT_MOVED:
                    position = _position
                    world[position] = SPACE_VOID
                elif event == EVENT_MOVED_OXYGEN:
                    position = _position
                    world[position] = SPACE_OXYGEN
                    return position
                elif event == EVENT_NO_MOVE:
                    world[_position] = SPACE_WALL
                    # Change direction
                    break



def main():
    args = parse_args()
    data = read_csv_int(data_file_path_main(test=False), to_list=True)

    log_always("Part 1")
    oxygen_position = find_oxygen(data)
    print(oxygen_position)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
