#!/usr/bin/env python3

import sys
import traceback
import numpy as np

from common.utils import *


def print_grid(grid, step=None):
    if step is not None:
        log.always(f"Step {step}:")
    for row in grid:
        log.always("".join(["#" if c else "." for c in row]))
    log.always("")


def iterate(grid, n=1, verbose=False, part2=False):
    mask = np.zeros(grid.shape, dtype=bool)
    if part2:
        mask[0, 0] = True
        mask[-1, 0] = True
        mask[0, -1] = True
        mask[-1, -1] = True

    grid = grid + mask
    if verbose:
        print_grid(grid, step=0)

    for i in range(n):
        _grid = grid.astype(int)
        _grid = _grid + np.pad(_grid[:, :-1], ((0, 0), (1, 0))) + np.pad(_grid[:, 1:], ((0, 0), (0, 1)))
        _grid = _grid + np.pad(_grid[:-1, :], ((1, 0), (0, 0))) + np.pad(_grid[1:, :], ((0, 1), (0, 0)))
        _grid -= grid.astype(int)
        grid = ((_grid == 2) * grid) + (_grid == 3) + mask
        if verbose:
            print_grid(grid, step=i + 1)

    return grid


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)
    grid = np.array([[c == "#" for c in line] for line in lines])
    verbose = args.verbose >= 3

    log.always("Part 1")
    n = 4 if args.test else 100
    _grid = iterate(grid, n, verbose=verbose)
    result = np.sum(_grid)
    log.always(result)

    log.always("Part 1")
    n = 5 if args.test else 100
    _grid = iterate(grid, n, verbose=verbose, part2=True)
    result = np.sum(_grid)
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
