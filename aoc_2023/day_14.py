#!/usr/bin/env python3
import copy
import sys
import traceback
from common.utils import *


ROCK = "O"
FIXED = "#"
VOID = "."


def compact(data):
    _data = copy.deepcopy(data)
    y_max = len(data)
    for x in range(len(_data[0])):
        log.debug(f"Processing row {x}")
        start = 0
        rocks = 0
        for y in range(y_max + 1):
            if y >= y_max or _data[y][x] == FIXED:
                log.debug(f"Fixed rock at {y}, with {rocks} rocks")
                for _y in range(start, y):
                    _data[_y][x] = ROCK if ((_y - start) < rocks) else VOID
                start = y + 1
                rocks = 0
            elif _data[y][x] == ROCK:
                rocks += 1
    return _data


def rotate(data):
    return [[data[y][x] for y in reversed(range(len(data)))] for x in range(len(data[0]))]


def calculate_score(data):
    result = 0
    y_max = len(data)
    for x in range(len(data[0])):
        for y in range(y_max):
            if data[y][x] == ROCK:
                result += y_max - y
    return result


def solve_part1(data):
    data = compact(data)
    return calculate_score(data)


MIN_PATTERN_LEN = 4
PATTERN_REPEATS = 4
ITERATIONS = 1000000000


def solve_part2(data):
    scores = []
    for i in range(ITERATIONS):
        # Check if scores has a pattern
        if (i % PATTERN_REPEATS) == 0 and i >= (PATTERN_REPEATS * MIN_PATTERN_LEN):
            pattern_len = int(i / PATTERN_REPEATS)
            _scores = list(grouper(scores, pattern_len))[1:]
            _scores_repeat = _scores[0]
            for j in range(1, len(_scores)):
                if not _scores_repeat == _scores[j]:
                    break
            else:
                n = (ITERATIONS - 1) % len(_scores_repeat)
                return _scores_repeat[n]
        # Perform new round of rotations, calculate score
        for n in range(4):
            data = compact(data)
            data = rotate(data)
        score = calculate_score(data)
        scores.append(score)
    # Didn't find a repeating pattern? Return the last score
    return scores[-1]


def main():
    args = parse_args()
    data = read_lines(input_file_path_main(test=args.test), to_list=True)
    data = [list(row) for row in data]

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data)
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
