#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from common.pygame_visualise import *
from intcode_vm import *


DIRECTION_NORTH = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3
DIRECTION_EAST = 4

DIRECTIONS = [
    DIRECTION_NORTH,
    DIRECTION_SOUTH,
    DIRECTION_WEST,
    DIRECTION_EAST,
]

EVENT_NO_MOVE = 0
EVENT_MOVED = 1
EVENT_MOVED_OXYGEN = 2


class Visualiser(PyGameVisualise):
    def __init__(self):
        super().__init__(60, 60, 10, Color.GREY)

    def draw_block(self, x, y, color, gap=0):
        # Offset coordinates before drawing
        x += round(self._x / 2)
        y += round(self._y / 2)
        if 0 <= x < self._x and 0 <= y < self._y:
            super().draw_block(x, y, color, gap)


def position_move(position, direction):
    x, y = position
    y += 1 if direction == DIRECTION_NORTH else -1 if direction == DIRECTION_SOUTH else 0
    x += 1 if direction == DIRECTION_EAST else -1 if direction == DIRECTION_WEST else 0
    return x, y


def map_world(data, visualiser=None):
    """ Part 1: Map the world by creating a VM and using flood filling
        Returns:
            paths: position:distance pairs for every world position that is path
            walls: set of positions for every wall found
            oxygen_position: position of oxygen (if found)
            oxygen_vm: VM at oxygen_position (if found)
    """
    vm = VM(data)
    start = (0, 0)
    paths = {start: 0}
    walls = set()
    oxygen_position = None
    oxygen_vm = None

    def callback(event, position, distance, _vm):
        # Update oxygen information if necessary
        nonlocal oxygen_position, oxygen_vm
        if event == EVENT_MOVED_OXYGEN:
            oxygen_position = position
            oxygen_vm = _vm
        # Visualise
        if visualiser is not None:
            visualiser.fill(Color.GREY)
            for coord in walls:
                visualiser.draw_block(*coord, Color.BLACK, gap=1)
            for coord in paths.keys():
                visualiser.draw_block(*coord, Color.WHITE, gap=1)
            visualiser.draw_block(0, 0, Color.RED, gap=1)
            if oxygen_position is not None:
                visualiser.draw_block(*oxygen_position, Color.GREEN, gap=1)
            visualiser.draw()

    simulate(vm, start, 0, paths, walls, callback)
    return paths, walls, oxygen_position, oxygen_vm


def flood_oxygen(oxygen_position, oxygen_vm, paths, walls, visualiser=None):
    """ Part 2: Flood from oxygen_position.
        Return (position, distance) dictionary with distances relative to oxygen_vm start location
    """
    oxygen_paths = {oxygen_position: 0}

    def callback(event, position, distance, _vm):
        # Visualise
        if visualiser is not None:
            visualiser.fill(Color.GREY)
            for coord in walls:
                visualiser.draw_block(*coord, Color.BLACK, gap=1)
            for coord in paths.keys():
                visualiser.draw_block(*coord, Color.WHITE, gap=1)
            visualiser.draw_block(0, 0, Color.RED, gap=1)
            for coord in oxygen_paths.keys():
                visualiser.draw_block(*coord, Color.ORANGE, gap=1)
            if oxygen_position is not None:
                visualiser.draw_block(*oxygen_position, Color.GREEN, gap=1)
            visualiser.draw()

    simulate(oxygen_vm, oxygen_position, 0, oxygen_paths, walls, callback)
    return oxygen_paths


def simulate(vm, start_position, start_distance, paths, walls, callback):
    """ Map flood world with vm. All positions are relative to start_position, which denotes vm starting location
        paths is updated with position:distance pairs for every world position that is path
        walls is updated with positions for every wall found
        event_callback is called with every new location discovered, with args (event, position, distance, vm)
    """
    path_heads = HeapQ([(start_distance, start_position, vm)])
    while path_heads:
        # Dijkstra: expand from the position with lowest distance
        distance, position, vm = path_heads.pop()
        _distance = distance + 1
        for direction in DIRECTIONS:
            _position = position_move(position, direction)
            if _position in walls or _position in paths:
                continue
            # Make a copy of the current vm and move it in direction
            _vm = vm.clone()
            _vm.input.put(direction)
            event = _vm.run_until_output()

            if event in [EVENT_MOVED, EVENT_MOVED_OXYGEN]:
                # Mark new path and add new position to queue
                paths[_position] = _distance
                path_heads.push((_distance, _position, _vm))
            elif event == EVENT_NO_MOVE:
                # Mark wall
                walls.add(_position)
            else:
                raise RuntimeError(f"Invalid output? {event}")
            callback(event, _position, _distance, _vm)


def main():
    args = parse_args()
    data = read_csv_int(input_file_path_main(test=False), to_list=True)
    visualiser = Visualiser() if args.verbose else None

    log.always("Part 1")
    paths, walls, oxygen_position, oxygen_vm = map_world(data, visualiser)
    if oxygen_position is not None:
        log.always(paths[oxygen_position])
        log.always("Part 2")
        oxygen_paths = flood_oxygen(oxygen_position, oxygen_vm, paths, walls, visualiser)
        log.always(max(oxygen_paths.values()))

    if visualiser is not None:
        visualiser.check_quit(5)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
