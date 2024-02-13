#!/usr/bin/env python3

import contextlib
import dataclasses
import math
import sys
import traceback
from typing import TypeAlias

from common.utils import *

import sympy


@dataclasses.dataclass
class Vector:
    x0: int
    y0: int
    z0: int
    vx: int
    vy: int
    vz: int

    @property
    def xy_m(self):
        """ Gradient in x-y plane """
        return self.vy / self.vx

    @property
    def xy_c(self):
        """ y value when x=0 """
        return self.y0 - (self.x0 * self.xy_m)

    def calc_y(self, x):
        if (self.vx > 0) ^ (x >= self.x0):
            raise ValueError(f"{x} is in the past")
        return self.xy_m * x + self.xy_c


Vectors: TypeAlias = list[Vector]


def calculate_intersection(v1: Vector, v2: Vector):
    if math.isclose(v1.xy_m, v2.xy_m):
        raise ValueError(f"Vectors are parallel")
    x = (v2.xy_c - v1.xy_c) / (v1.xy_m - v2.xy_m)
    y = v1.calc_y(x)
    _y = v2.calc_y(x)
    assert math.isclose(y, _y), f"Error calculating intersect: {y} != {_y}"
    return x, y


def solve_part1(vectors: Vectors, min_value, max_value):
    result = 0
    for i, v1 in enumerate(vectors):
        for j in range(i + 1, len(vectors)):
            v2 = vectors[j]
            with contextlib.suppress(ValueError):
                x, y = calculate_intersection(v1, v2)
                log.debug(f"{i} ({v1}) \tand \t{j} ({v2}) \tintersect at \t{x, y}")
                if min_value <= x <= max_value and min_value <= y <= max_value:
                    result += 1
    return result


def solve_part2(vectors: Vectors):
    # Create symbols for thrown stone vector
    x0 = sympy.Symbol('x')
    y0 = sympy.Symbol('y')
    z0 = sympy.Symbol('z')
    vx = sympy.Symbol('vx')
    vy = sympy.Symbol('vy')
    vz = sympy.Symbol('vz')
    symbols = [x0, y0, z0, vx, vy, vz]
    equations = []
    for i, v in enumerate(vectors[:3]):
        # Create equations time of intercept between stone and vector
        t = sympy.Symbol(f"t{i}")
        symbols.append(t)
        equations.extend([
            ((x0 + vx * t) - (v.x0 + v.vx * t)),
            ((y0 + vy * t) - (v.y0 + v.vy * t)),
            ((z0 + vz * t) - (v.z0 + v.vz * t)),
        ])
    solutions = sympy.solve_poly_system(equations, symbols)
    if len(solutions) == 0:
        log.error(f"No solutions found")
        return None
    solution = solutions[0][:6]
    log.info(f"Solution: {solution}")
    val_x0, val_y0, val_z0, *_ = solution
    return val_x0 + val_y0 + val_z0


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)
    vectors = [
        Vector(*map(int, line.replace(" @", ",").split(",")))
        for line in lines
    ]

    log.always("Part 1:")
    result = solve_part1(vectors, *([7, 27] if args.test else [200000000000000, 400000000000000]))
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(vectors)
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
