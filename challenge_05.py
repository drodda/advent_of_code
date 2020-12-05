#!/usr/bin/env python3

import os
import sys
import traceback
import ipdb as pdb
import re
import json
import numpy as np

from utils import *


BITS_ROW = 7
BITS_COL = 3

N_SEATS = pow(2, BITS_ROW + BITS_COL)


def calculate_seat_id(row, col):
    return row * 8 + col


class InvalidSeat(Exception):
    def __init__(self, text):
        super().__init__(f"Invalid seat: {text}")


def decode_bin_str(text, zero_char, one_char):
    text_bin = text.replace(zero_char, "0").replace(one_char, "1")
    if not re.match(r"^[01]+$", text_bin):
        raise InvalidSeat(text)
    return int(text_bin, 2)


def parse_seat(text):
    row_text = text[:BITS_ROW]
    col_text = text[BITS_ROW:BITS_ROW + BITS_COL]

    row = decode_bin_str(row_text, "F", "B")
    col = decode_bin_str(col_text, "L", "R")

    seat_id = calculate_seat_id(row, col)

    print_debug(f"{text} = {row},{col} = {seat_id}")
    return row, col, seat_id


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test))

    max_seat_id = 0
    seat_array = np.zeros(N_SEATS, dtype=np.bool)
    for line in lines:
        try:
            row, col, seat_id = parse_seat(line)
        except InvalidSeat as e:
            print_debug(str(e))
        else:
            max_seat_id = max(max_seat_id, seat_id)
            seat_array[seat_id] = True

    print("Part 1:")
    print(max_seat_id)

    print("Part 2:")

    missing_seats = np.where(seat_array==False)[0]
    for missing_seat in missing_seats:
        if (missing_seat + 1) not in missing_seats and (missing_seat - 1) not in missing_seats:
            print(f"Missing seat: {missing_seat}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
