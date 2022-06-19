#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *
from intcode_vm import *


DIR_RIGHT = (0, 1)
DIR_DOWN = (1, 0)
DIR_LEFT = (0, -1)
DIR_UP = (-1, 0)
DIRS = (DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP)
DIR_REVERSE_MAP = {
    DIR_RIGHT: DIR_LEFT,
    DIR_LEFT: DIR_RIGHT,
    DIR_DOWN: DIR_UP,
    DIR_UP: DIR_DOWN,
}
DIR_TURN_MAP = {
    DIR_RIGHT: {DIR_UP: "L", DIR_DOWN: "R"},
    DIR_LEFT: {DIR_UP: "R", DIR_DOWN: "L"},
    DIR_DOWN: {DIR_RIGHT: "L", DIR_LEFT: "R"},
    DIR_UP: {DIR_RIGHT: "R", DIR_LEFT: "L"},
}

SYM_SCAFFOLD = "#"
SYM_SPACE = "."
SYM_ROBOT_RIGHT = ">"
SYM_ROBOT_DOWN = "v"
SYM_ROBOT_LEFT = "<"
SYM_ROBOT_UP = "^"
SYM_ROBOT_DEAD = "X"
SYMS_ROBOT = [SYM_ROBOT_RIGHT, SYM_ROBOT_DOWN, SYM_ROBOT_LEFT, SYM_ROBOT_UP, SYM_ROBOT_DEAD]
SYM_SCAFFOLD_ROBOT = [SYM_SCAFFOLD] + SYMS_ROBOT

SYM_DIR_MAP = {
    SYM_ROBOT_RIGHT: DIR_RIGHT,
    SYM_ROBOT_DOWN: DIR_DOWN,
    SYM_ROBOT_LEFT: DIR_LEFT,
    SYM_ROBOT_UP: DIR_UP,
}


def add2d(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def neighbours(pos):
    for _dir in DIRS:
        yield add2d(pos, _dir)


def solve_part1(world):
    def is_intersection(pos):
        if world[pos] not in SYM_SCAFFOLD_ROBOT:
            return False
        for _pos in neighbours(pos):
            if world[_pos] not in SYM_SCAFFOLD_ROBOT:
                return False
        return True
    result = 0
    for i in range(1, len(world) - 1):
        for j in range(1, len(world[i]) - 1):
            if is_intersection((i, j)):
                result += i * j
    return result


def world_find_start(world):
    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] in SYMS_ROBOT:
                return i, j
    return None


# def world_find_end(world):
#     for i in range(len(world)):
#         for j in range(len(world[i])):
#             if world[i][j] == SYM_SCAFFOLD:
#                 scaffold_neigh
#                 neighbours()
#                 return i, j
#     return None


def in_world(world, pos):
    return 0 <= pos[0] < world.shape[0] and 0 <= pos[1] < world.shape[1]


def path_world(world):
    # Find start
    start = world_find_start(world)

    # Find path
    pos = start
    _dir = SYM_DIR_MAP[world[pos]]
    path = []
    while True:
        # Find direction to follow
        for _dir_next in DIRS:
            if _dir_next == DIR_REVERSE_MAP[_dir]:
                # Direction we came from - ignore
                continue
            if in_world(world, add2d(pos, _dir_next)) and world[add2d(pos, _dir_next)] == SYM_SCAFFOLD:
                break
        else:
            # No more paths
            break
        turn = (DIR_TURN_MAP[_dir][_dir_next])
        _dir = _dir_next
        # Find distance
        i = 0
        while in_world(world, add2d(pos, _dir)) and world[add2d(pos, _dir)] != SYM_SPACE:
            i += 1
            pos = add2d(pos, _dir)

        path.append((turn, i))
    return path


def tokenise(path):
    def combine_path(_token):
        return ",".join([f"{_dir},{int(_dist)}" for _dir, _dist in _token])

    for a in range(1, 11):
        token_a = path[:a]
        for b in range(1, 11):
            token_b = path[a:a + b]

            # Find first occurrence of not token_a or token_b
            i = a + b
            while True:
                if path[i:i + a] == token_a:
                    i += a
                elif path[i:i + b] == token_b:
                    i += b
                else:
                    break
            # Find token_c: all symbols until next token_a or token_b
            token_c = None
            for c in range(1, 11):
                if path[i + c:i + c + a] == token_a or path[i + c:i + c + b] == token_b:
                    token_c = path[i:i + c]
                    break
            else:
                # No token c - try a and b again
                break
            # Tokenise!
            result = []
            i = 0
            while i < len(path):
                if (i + a) <= len(path) and path[i:i + a] == token_a:
                    result.append("A")
                    i += a
                elif (i + b) <= len(path) and path[i:i + b] == token_b:
                    result.append("B")
                    i += b
                elif (i + c) <= len(path) and path[i:i + c] == token_c:
                    result.append("C")
                    i += c
                else:
                    # No token found - abort
                    break
            else:
                return ",".join(result), combine_path(token_a), combine_path(token_b), combine_path(token_c)

    raise IndexError("No solution")


def solve_part2(data, world):
    path = path_world(world)
    tokens, token_a, token_b, token_c = tokenise(path)
    # Run simulation
    vm = VM(data)
    vm.mem_put(0, 2)
    for line in [tokens, token_a, token_b, token_c]:
        log_verbose(line)
        for c in line:
            vm.input.put(ord(c))
        vm.input.put(ord("\n"))
    vm.input.put(ord("n"))
    vm.input.put(ord("\n"))
    vm.run()
    data = list(vm.output.queue)
    return data[-1]


def print_world(world):
    for row in world:
        log_info("".join(row))


def main():
    args = parse_args()
    data = read_csv_int(data_file_path_main(test=False), to_list=True)
    log_always("Part 1")
    vm = VM(data)
    vm.run()
    world_txt = "".join([chr(c) for c in vm.output.queue]).splitlines()
    world = np.array([list(line) for line in world_txt if line])
    if args.verbose:
        print_world(world)
        # for line in world:
        #     log_info(line)
    result = solve_part1(world)
    log_always(result)
    log_always("Part 2")
    result = solve_part2(data, world)
    log_always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
