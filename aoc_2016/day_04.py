#!/usr/bin/env python3
import collections
import functools
import string
import sys
import traceback
from common.utils import *


def comparator(item1, item2):
    char1, count1 = item1
    char2, count2 = item2
    if count1 == count2:
        return 1 if char1 > char2 else 0 if char1 == char2 else -1
    return 1 if count1 < count2 else 0 if count1 == count2 else -1


def decode(s, checksum):
    return "".join([
        chr((ord(c) - ord("a") + checksum) % 26 + ord("a")) if c in string.ascii_lowercase else " " if c == "-" else c
        for c in s
    ])


def solve(lines):
    result1 = 0
    result2 = None
    for line in lines:
        encoded_room_label, sector_id, checksum,  = line.rstrip("]").replace("[", "-").rsplit("-", 2)
        sector_id = int(sector_id)
        chars = encoded_room_label.replace("-", "")
        char_count = collections.Counter(chars)
        char_count_sorted = sorted(char_count.items(), key=functools.cmp_to_key(comparator))
        calculated_checksum = "".join([item[0] for item in char_count_sorted[:5]])
        if calculated_checksum == checksum:
            result1 += sector_id
            room_label = decode(encoded_room_label, sector_id)
            log.debug(f"{sector_id}\t{room_label}")
            if "northpole" in room_label:
                log.info(f"Found room: {room_label}")
                result2 = sector_id
    return result1, result2


def main():
    args = parse_args()
    lines = read_lines(input_file_path_main(test=args.test), to_list=True)

    result1, result2 = solve(lines)

    log.always("Part 1:")
    log.always(result1)

    log.always("Part 2:")
    log.always(result2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
