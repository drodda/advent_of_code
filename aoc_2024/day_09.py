#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def solve_part1(data):
    # Construct non-sparse disk
    disk = []
    for i, c in enumerate(data):
        n = int(c)
        if i % 2 == 0:
            # File
            file_id = int(i / 2)
            disk.extend([file_id] * n)
        else:
            # Free space
            disk.extend([None] * n)
    # Move blocks from tail of disk to left-most free block
    head = 0
    tail = len(disk) - 1
    while head < tail:
        if disk[head] is not None:
            head += 1
        elif disk[tail] is None:
            tail -= 1
        else:
            disk[head] = disk[tail]
            disk[tail] = None
    # Calculate checksum
    result = 0
    for i, val in enumerate(disk):
        if val is not None:
            result += i * val
    return result


def solve_part2(data):
    # Construct sparse disk
    current_block_index = 0
    files = {}  # (start block, file length) for each file
    free_chunks = {}  # Free space at block index
    for i, c in enumerate(data):
        n = int(c)
        if i % 2 == 0:
            # File
            file_id = int(i / 2)
            files[file_id] = (current_block_index, n)
            # file_index[file_id] = current_block_index
            # file_lens[file_id] = n
        else:
            # Free space
            free_chunks[current_block_index] = n
        current_block_index += n
    # Try to move each block once
    for file_id, (file_start, file_len) in reversed(files.items()):
        # Search forward in free space to find a free chunk that will fit file_len
        for free_space_start in sorted(free_chunks):
            free_space_size = free_chunks[free_space_start]
            if free_space_size >= file_len:
                # Move block only if found gap is less than current position
                if free_space_start < file_start:
                    files[file_id] = (free_space_start, file_len)
                    # Remove free chunk
                    del free_chunks[free_space_start]
                    free_space_size -= file_len
                    free_space_start += file_len
                    # Add new free chunk for remaining free blocks
                    if free_space_size > 0:
                        free_chunks[free_space_start] = free_space_size
                break
    # Calculate checksum
    result = 0
    for file_id, (file_start, file_len) in reversed(files.items()):
        for i in range(file_len):
            result += file_id * (file_start + i)
    return result


def main():
    args = parse_args()
    data = open(args.input).read().strip()

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
