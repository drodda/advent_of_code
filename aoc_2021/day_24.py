#!/usr/bin/env python3

import sys
import traceback

from common.utils import *

"""
The ALU code appear to be in blocks of 18 instructions which is repeated 14 times. 
Each block follows the following template with only a few different instructions:
    0   inp w
    1   mul x 0
    2   add x z
    3   mod x 26
    4   div z <ZZ: 1 or 26>
    5   add x <XX>
    6   eql x w
    7   eql x 0
    8   mul y 0
    9   add y 25
    10  mul y x
    11  add y 1
    12  mul z y
    13  mul y 0
    14  add y w
    15  add y <YY>
    16  mul y x
    17  add z y

Blocks can increment z (if ZZ is 1) or decrement z (if ZZ is 26)

This is equivalent to:
    x = 0 if ((z % 26) + xx) == INPUT_DIGIT else 1
    z = z / ZZ
    z = z * ((25 * x) + 1) + (x * (INPUT_DIGIT + YY))

Z will grow unless ZZ is 26 in which case it _can_ decrease, but only if ((z % 26) + xx) == INPUT_DIGIT

"""


BLOCK_SIZE = 18


def eval_block(block, digit, z):
    """ Evaluates a single block with a given digit and z. Return z after evaluation """
    zz, xx, yy = block
    x = 0 if ((z % 26) + xx) == digit else 1
    z = z // zz
    z = z * ((25 * x) + 1) + (x * (digit + yy))
    return z


def solve(block_values, i=0, z=0, largest=True):
    """ Determine the (largest or smallest) digigts required to run the rest of the program with a given z,
        which results in z=0 at the end of the program

        i is the index into block_values for the current processing step.
        
        Returns digits for the (largest or smallest) solution from (block_i, z)
        Returns 0 on if no solution exists for the (block_i, z) combination
    """

    # Digit search order, to provide the largest or smallest input value
    digits = list(range(9, 0, -1)) if largest else list(range(1, 10))

    block = block_values[i]
    zz, xx, yy = block

    if i == len(block_values) - 1:
        for digit in digits:
            if eval_block(block, digit, z) == 0:
                return digit
        return 0
    if zz == 26:
        # Decrease block: INPUT_DIGIT must be ((z % 26) + xx)
        _digit = (z % 26) + xx
        if _digit < 1 or _digit > 9:
            return 0
        digits = [_digit]

    for digit in digits:
        _z = eval_block(block, digit, z)
        res = solve(block_values, i + 1, _z, largest)
        if res > 0:
            return (digit * (10 ** (13 - i))) + res
    return 0


def main():
    args = parse_args()
    data_raw = read_lines(args.input)

    instructions = [line.split(" ") for line in data_raw]
    # Extract only the values from each block that are different
    block_values = [
        (int(instructions[i + 4][2]), int(instructions[i + 5][2]), int(instructions[i + 15][2]))
        for i in range(0, len(instructions), BLOCK_SIZE)
    ]

    log.always("Part 1:")
    result = solve(block_values, largest=True)
    log.always(result)

    log.always("Part 2:")
    result = solve(block_values, largest=False)
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
