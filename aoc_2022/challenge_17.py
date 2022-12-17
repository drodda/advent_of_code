#!/usr/bin/env python3

import sys
import traceback
import numpy as np
from common.utils import *


def parse_input(test=False):
    data = open(data_file_path_main(test=test)).read().strip()
    # Convert to +1 / -1
    data = [1 if v == ">" else -1 for v in data]
    return data


ROCKS = [
    np.array([[1, 1, 1, 1]], dtype=bool),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool),
    np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]], dtype=bool),
    np.array([[1], [1], [1], [1]], dtype=bool),
    np.array([[1, 1], [1, 1]], dtype=bool),
]

ROCK_HEIGHTS = [
    np.array([1, 1, 1, 1], dtype=int),
    np.array([2, 3, 2], dtype=int),
    np.array([1, 1, 3], dtype=int),
    np.array([4], dtype=int),
    np.array([2, 2], dtype=int),
]


def is_collision(world, rock, x, y):
    return np.any(world[y: y + rock.shape[0], x:x + rock.shape[1]] * rock)


def solve(winds):
    n_rounds_1 = 2022
    n_rounds_2 = 1000000000000
    world = np.zeros([1024, 7], dtype=bool)
    # Set floor
    height = 0
    i = 1
    seen = {}
    heights = {}
    rock_i = 0
    wind_i = 0
    top_heights = np.zeros(7, dtype=int)
    while True:
        # Check for repeated state: (rock index, wind index, normalised height of each column)
        if (rock_i, wind_i, tuple(top_heights)) in seen:
            _i, _height = seen[(rock_i, wind_i, tuple(top_heights))]
            n_reps, n_rocks = divmod(n_rounds_1 - i, i - _i)
            _result_1 = height + (height - _height) * n_reps + (heights[_i + n_rocks + 1] - heights[_i])
            n_reps, n_rocks = divmod(n_rounds_2 - i, i - _i)
            _result_2 = height + (height - _height) * n_reps + (heights[_i + n_rocks + 1] - heights[_i])
            return _result_1, _result_2
        seen[(rock_i, wind_i, tuple(top_heights))] = (i, height)
        heights[i] = height

        rock = ROCKS[rock_i]
        x = 2
        y = height + 3
        if y > world.shape[0] - rock.shape[0]:
            _world = np.zeros([world.shape[0] + 1024, world.shape[1]], dtype=bool)
            _world[:world.shape[0], :] = world
            world = _world
        while True:
            # Move from wind
            wind_dir = winds[wind_i]
            wind_i = (wind_i + 1) % len(winds)
            _x = x + wind_dir
            if 0 <= _x <= (world.shape[1] - rock.shape[1]) and not is_collision(world, rock, _x, y):
                x = _x
            # Fall (if possible)
            _y = y - 1
            if _y < 0 or is_collision(world, rock, x, _y):
                break
            y = _y
        # Calculate change in height
        dy = max(0, y - height + rock.shape[0])
        # Adjust top_heights
        top_heights[x:x + rock.shape[1]] = ROCK_HEIGHTS[rock_i] + y - height
        top_heights -= dy

        # Add rock to world
        world[y: y + rock.shape[0], x:x + rock.shape[1]] += rock

        # Adjust height
        height += dy

        rock_i = (rock_i + 1) % len(ROCKS)
        i += 1


def main():
    args = parse_args()
    # data = open(data_file_path_main(test=args.test)).read().strip()
    data = parse_input(test=args.test)

    result_1, result_2 = solve(data)
    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except (KeyboardInterrupt, BrokenPipeError):
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
