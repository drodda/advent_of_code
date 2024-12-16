#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def parse_world(data):
    start = None
    walls = set()
    boxes = set()
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            pos = (x, y)
            if c == "#":
                walls.add(pos)
            elif c == "O":
                boxes.add(pos)
            elif c == "@":
                start = pos
    return start, walls, boxes


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def solve_part1(data, moves):
    pos, walls, boxes = parse_world(data)
    for _dir in moves:
        _pos = move(pos, _dir)
        if _pos in boxes:
            # Keep moving until either a wall is discovered or empty space
            box_pos = _pos
            while box_pos in boxes:
                box_pos = move(box_pos, _dir)
            if box_pos not in walls:
                # Move boxes
                boxes.remove(_pos)
                boxes.add(box_pos)
                # Move robot
                pos = _pos
        elif _pos not in walls:
            pos = _pos
    result = 0
    for x, y in boxes:
        result += y * 100 + x
    return result


def expand_world(pos, walls, boxes):
    def double(_pos):
        return 2 * _pos[0], _pos[1]
    pos = double(pos)
    walls = {double(wall) for wall in walls}
    walls.update({move(wall, ">") for wall in walls})
    boxes = {double(box) for box in boxes}
    return pos, walls, boxes


def find_box(boxes, pos):
    if pos in boxes:
        return pos
    _pos = move(pos, "<")
    if _pos in boxes:
        return _pos
    return None


def move_box(box, _dir):
    _box = move(box, _dir)
    yield _box
    yield move(_box, ">")


def solve_part2(data, moves):
    pos, walls, boxes = parse_world(data)
    pos, walls, boxes = expand_world(pos, walls, boxes)

    for _dir in moves:
        _pos = move(pos, _dir)
        box = find_box(boxes, _pos)
        if box:
            # Collide with a box: try to move boxes
            moved_boxes = {box}
            to_move = {box, }
            success = True
            while to_move and success:
                box = to_move.pop()
                # Move the box
                for moved_box in move_box(box, _dir):
                    if moved_box in walls:
                        # Box moves into a wall: abort
                        success = False
                    else:
                        next_box = find_box(boxes, moved_box)
                        if next_box is not None and next_box not in moved_boxes:
                            moved_boxes.add(next_box)
                            to_move.add(next_box)
            if success:
                pos = _pos
                boxes.difference_update(moved_boxes)
                boxes.update({move(box, _dir) for box in moved_boxes})
        elif _pos not in walls:
            pos = _pos
    result = 0
    for x, y in boxes:
        result += y * 100 + x
    return result


def main():
    args = parse_args()
    data, moves = read_multilines(args.input)
    moves = "".join(moves)

    log.always("Part 1:")
    result = solve_part1(data, moves)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data, moves)
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
