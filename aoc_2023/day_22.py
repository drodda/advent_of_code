#!/usr/bin/env python3
import collections
import dataclasses
import sys
import traceback
from typing import Generator

from common.utils import *


@dataclasses.dataclass
class Brick:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def __repr__(self):
        return f"(({self.x1},{self.y1},{self.z1}):({self.x2},{self.y2},{self.z2}))"

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise NotImplemented
        return self.z1 < other.z1

    def xy_range(self) -> Generator[tuple, None, None]:
        for x in range(self.x1, self.x2 + 1):
            for y in range(self.y1, self.y2 + 1):
                yield x, y

    def drop(self, dz) -> "Brick":
        return dataclasses.replace(self, z1=self.z1 - dz, z2=self.z2 - dz)


def drop(bricks):
    max_z = collections.defaultdict(int)
    new_bricks = []
    n_falls = 0
    for brick in bricks:
        highest_z = max(max_z[xy] for xy in brick.xy_range())
        dz = max(brick.z1 - highest_z - 1, 0)
        new_brick = brick
        if dz > 0:
            new_brick = brick.drop(dz)
            log.debug(f"Dropping {brick} by {dz} = {new_brick}")
            n_falls += 1
        new_bricks.append(new_brick)
        for xy in new_brick.xy_range():
            max_z[xy] = new_brick.z2
    return new_bricks, n_falls


def solve(bricks):
    bricks = sorted(bricks)

    # Initially drop bricks
    bricks, _ = drop(bricks)
    log.debug(f"{bricks}")

    result_part1 = 0
    result_part2 = 0
    for i, brick in enumerate(bricks):
        _bricks = bricks[:i] + bricks[i + 1:]
        log.debug(f"{i}: Removing {brick} = {_bricks}")
        _, n_falls = drop(_bricks)
        log.debug(f"  {n_falls}")
        log.info(f"{i}: {n_falls}")
        if not n_falls:
            result_part1 += 1
        else:
            result_part2 += n_falls

    return result_part1, result_part2


def main():
    args = parse_args()
    bricks = [
        Brick(*map(int, line.replace("~", ",").split(",")))
        for line in read_lines(args.input)
    ]

    result_part1, result_part2 = solve(bricks)
    log.always("Part 1:")
    log.always(result_part1)

    log.always("Part 2:")
    log.always(result_part2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
