#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


AMPHIPODS = ["A", "B", "C", "D"]

COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def state_to_str(state):
    """ Convert state to string """
    return "\n".join(state)


def state_from_str(state_str):
    """ Convert state string to state """
    return state_str.split("\n")


def generate_desired_state(state_str):
    """ Generate the desired solution state string from a given state """
    state = state_from_str(state_str)
    return state_to_str([state[0]] + ["##A#B#C#D##"] * (len(state) - 1))


def can_move_through_hallway(state, x1, x2):
    """ Return True if amphipod at x1 in the hallway can move to x2 without obstruction """
    return all([space == "." for space in (state[0][x1 + 1:x2 + 1] + state[0][x2:x1])])


def generate_move(cost, state, x1, y1, x2, y2):
    """ Generate a new cost and state moving amphipod from (x1, y1) to (x2, y2) """
    amphipod = state[y1][x1]
    _cost = cost + COSTS[amphipod] * (abs(x2 - x1) + abs(y2 - y1))
    _state = []
    for i, line in enumerate(state):
        if i == y1:
            line = line[:x1] + "." + line[x1 + 1:]
        if i == y2:
            line = line[:x2] + amphipod + line[x2 + 1:]
        _state.append(line)
    return _cost, state_to_str(_state)


def generate_moves_out_of_room(cost, state, x, y):
    """ Generate all moves for amphipod at (x, y) to move out of the room into the hallway
        (x, y) must be an amphipod in a room
    """
    result = []
    # Generate a new state without the amphipod at x, y
    if y == 1 or state[y - 1][x] == ".":
        _y = 0
        for _x in [0, 1, 3, 5, 7, 9, 10]:
            if can_move_through_hallway(state, x, _x):
                result.append(generate_move(cost, state, x, y, _x, _y))
    return result


def generate_move_into_room(cost, state, x, y):
    """ Generates a move for amphipod at (x, y) into their target room from the hallway
        (x, y) must be an amphipod in the hallway
        Returns None if amphipod at (x, y) can not move into their target room
    """
    amphipod = state[y][x]
    # Check if this amphipod can move into it's target room
    _x = AMPHIPODS.index((amphipod)) * 2 + 2
    if can_move_through_hallway(state, x, _x) and all([line[_x] in [".", amphipod] for line in state[1:]]):
        # Generate a new state without the amphipod at x, y
        _y = max([i for i in range(len(state)) if state[i][_x] == "."])
        return generate_move(cost, state, x, y, _x, _y)
    return None


def generate_moves(cost, state_str):
    """ Generate all possible moves from state defined by state_str """
    state = state_from_str(state_str)
    result = []
    for x, c in enumerate(state[0]):
        if c in AMPHIPODS:
            move = generate_move_into_room(cost, state, x, 0)
            if move is not None:
                result.append(move)
    for i, line in enumerate(state[1:]):
        y = i + 1
        for x, c in enumerate(line):
            if c in AMPHIPODS:
                result.extend(generate_moves_out_of_room(cost, state, x, y))
    return result


def solve(input_text):
    state_str = state_to_str([input_text[1][1:-1]] + ["#" + line.strip().replace("###", "#") + "#" for line in input_text[2:-1]])
    desired_state_str = generate_desired_state(state_str)
    steps = HeapQ([(0, state_str)])
    seen = set()
    result = None
    while steps:
        cost, state_str = steps.pop()
        if state_str == desired_state_str:
            result = cost
            break
        if state_str in seen:
            continue
        seen.add(state_str)
        for _cost, _state_str in generate_moves(cost, state_str):
            steps.push((_cost, _state_str))
    return result


def main():
    args = parse_args()
    data = read_lines(args.input, to_list=True)

    log.always("Part 1:")
    log.always(solve(data))

    log.always("Part 2:")
    data = data[:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + data[3:]
    log.always(solve(data))


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)

