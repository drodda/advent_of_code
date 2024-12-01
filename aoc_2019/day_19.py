#!/usr/bin/env python3

import sys
import traceback

from common.utils import *
from intcode_vm import *


PART_1_MAX = 50
START_ROW = 10
GRID_SIZE = 100


class BeamFinder:
    def __init__(self, data):
        self.data = data
        self._row_starts = {}
        self._row_ends = {}

    def run_beam(self, x, y):
        vm = VM(self.data, input_queue=[x, y])
        return vm.run_until_output()

    def row_start(self, y, search_min=None, search_max=None):
        if y in self._row_starts:
            return self._row_starts[y]
        x = search_min
        if x is None:
            x = self._row_starts.get(y - 1, 0)
        while True:
            if search_max is not None and x >= search_max:
                break
            if self.run_beam(x, y) == 1:
                self._row_starts[y] = x
                return x
            x += 1
        return None

    def row_end(self, y, search_max=None):
        if y in self._row_ends:
            return self._row_ends[y]
        start = self.row_start(y, search_max=search_max)
        if start is None:
            return None
        x = max(start, self._row_ends.get(y - 1, 0))
        while True:
            if search_max is not None and x >= search_max:
                break
            if self.run_beam(x + 1, y) == 0:
                self._row_ends[y] = x
                return x
            x += 1
        return None


def print_row(y, start, end, row_max):
    line = "." * row_max
    count = 0
    if start is not None:
        if end is None:
            end = row_max - 1
        count = end - start + 1
        tail = row_max - end - 1
        line = "." * start + "#" * count + "." * tail
    log.info(f"{y: 5d} {count: 5d} {line}")


def solve_part1(beam_finder, verbose=False):
    result = 0
    is_tail = False
    for y in range(PART_1_MAX):
        start = beam_finder.row_start(y, search_max=PART_1_MAX)
        end = beam_finder.row_end(y, search_max=PART_1_MAX)
        if start is not None:
            if end is None:
                end = PART_1_MAX - 1
                is_tail = True
            result += end - start + 1
        if verbose:
            print_row(y, start, end, PART_1_MAX)
        if start is None and is_tail:
            break
    return result


def solve_part2(beam_finder, test=False):
    grid_size = 10 if test else GRID_SIZE
    # The first few rows may not contain any beam - start at START_ROW
    y = START_ROW

    # Pre-scan GRID_SIZE rows to pre-calculate row start
    for _y in range(y, y + grid_size):
        beam_finder.row_start(_y)

    # Scan until a grid of GRID_SIZE fits in beam
    while True:
        x = beam_finder.row_start(y + grid_size - 1)
        end = beam_finder.row_end(y)
        log.debug(f"Row {y} {beam_finder.row_start(y)}:{end}, {y + grid_size - 1}: {x}")
        if (end - x + 1) >= grid_size:
            log.info(f"Solution {x}:{x + grid_size + 1} {y}:{y + grid_size - 1}")
            return x * 10000 + y
        y += 1


def main():
    args = parse_args()
    data = read_csv_int(args.input, to_list=True)
    beam_finder = BeamFinder(data)

    log.always("Part 1")
    result = solve_part1(beam_finder, verbose=(args.verbose >= 2))
    log.always(result)

    log.always("Part 2")
    result = solve_part2(beam_finder, test=args.test)
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
