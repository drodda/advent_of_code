#!/usr/bin/env python3

import collections
import sys
import traceback
from common.utils import *


DIRECTIONS = {
    "N": (0, -1),
    "NE": (1, -1),
    "E": (1, 0),
    "SE": (1, 1),
    "S": (0, 1),
    "SW": (-1, 1),
    "W": (-1, 0),
    "NW": (-1, -1),
}


MOVES = [
    ("N", ("N", "NE", "NW")),
    ("S", ("S", "SE", "SW")),
    ("W", ("W", "NW", "SW")),
    ("E", ("E", "NE", "SE")),
]


def move(pos, _dir):
    """ Move position 1 step in given direction """
    return pos[0] + DIRECTIONS[_dir][0], pos[1] + DIRECTIONS[_dir][1]


def elves_in_neighbours(elves, elf, dirs):
    """ Check if there are any elves in neighbouring directions """
    return any([(move(elf, _dir) in elves) for _dir in dirs])


def print_world(_round, elves):
    print(_round)
    xs = [x for x, y in elves]
    ys = [y for x, y in elves]
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            print("#" if (x, y) in elves else ".", end="")
        print()
    print()


def simulate(elves, moves):
    moved = collections.defaultdict(list)
    result = elves.copy()
    for elf in sorted(elves):
        # Only move if any elves are in any neighbouring positions
        if elves_in_neighbours(elves, elf, DIRECTIONS):
            for _dir, dirs in moves:
                if not elves_in_neighbours(elves, elf, dirs):
                    # Move elf in that direction
                    dest = move(elf, _dir)
                    log.debug(f"Attempting to move: {elf} {_dir} to {dest}")
                    moved[dest].append(elf)
                    result.remove(elf)
                    break
    # Determine which elves actually moved
    _moved = False
    for dest, _elves in moved.items():
        if len(_elves) == 1:
            # Move elf
            result.add(dest)
            log.debug(f"Moved: {_elves[0]} to {dest}")
            _moved = True
        else:
            # None of the elves get moved
            result = result.union(_elves)
            log.debug(f"Rejected move: {_elves} to {dest}")
    return result, _moved


def solve(data, verbose=False):
    # Convert elves to set of coordinates
    elves = set()
    for y, line in enumerate(data):
        for x, v in enumerate(line):
            if v == "#":
                elves.add((x, y))
    if verbose:
        print_world("Start", elves)

    # Run simulation until both parts are solved
    moves = MOVES
    i = 0
    result_1 = None
    result_2 = None
    while result_1 is None or result_2 is None:
        i += 1
        elves, moved = simulate(elves, moves)
        moves = moves[1:] + moves[:1]
        if not moved and result_2 is None:
            result_2 = i
        if verbose:
            print_world(f"Round {i}", elves)
        if i == 10:
            # Solve part 1
            xs = [x for x, y in elves]
            ys = [y for x, y in elves]
            result_1 = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) - len(elves)
    return result_1, result_2


def main():
    args = parse_args()
    data = read_lines(input_file_path_main(test=args.test), to_list=True)

    result_1, result_2 = solve(data, verbose=(args.verbose >= 1))

    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
