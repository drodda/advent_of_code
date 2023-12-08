#!/usr/bin/env python3
import collections
import sys
import traceback

from common.utils import *

# To merge a layer of transform:
# For existing transforms, if transform.dest in any new transform, apply transform
# Add new transforms where (any part of) transform.src not covered by existing transforms
# Order for convenience?


# ranges =
# src_start, src_end, dest_start, dest_end, offset


def merge_transform(ranges, transforms):
    # Map transforms onto existing ranges
    log.info(f"Ranges before applying transforms: {ranges}")
    result = []
    for range in ranges:
        _src_start, _src_end, _dest_start, _dest_end, _offset = range
        for src_start, src_end, dest_start, dest_end, offset in transforms:
            if _dest_start < src_start:
                # Add non-overlapping part of range (or full range) before transform without modification
                _len = min(src_start - _dest_start - 1, _dest_end - _dest_start)
                log.debug(f"Range before, not changed: {(_src_start, _src_start + _len, _offset)}")
                result.append((_src_start, _src_start + _len, _dest_start, _dest_start + _len, _offset))
                _src_start += _len + 1
                _dest_start += _len + 1
            # _dest_start must now be >= src_start
            if _dest_end >= src_start and _dest_start <= src_end:
                # Add overlapping part of range, with modified offset
                _len = min(_dest_end, src_end) - max(_dest_start, src_start)
                log.debug(f"Range changed: {_len} of {_src_start, _src_start + _len} = {_dest_start, _dest_start + _len} ({_offset}) by {src_start, src_end} ({offset})")
                result.append((_src_start, _src_start + _len, _dest_start, _dest_start + _len, _offset + offset))
                _src_start += _len + 1
                _dest_start += _len + 1
        # Add non-overlapping part of range (or full range) after all transforms without modification
        if _src_start <= _src_end:
            log.debug(f"Range after all transforms, not changed: {(_src_start, _src_end, _offset)}")
            result.append((_src_start, _src_end, _dest_start, _dest_end, _offset))

        # result.append(range)
    log.info(f"Ranges after applying transforms: {result}")

    # Apply new ranges for transforms that do not overlap existing ranges
    transforms_queue = collections.deque(transforms)
    while transforms_queue:
        transform = transforms_queue.pop()
        src_start, src_end, dest_start, dest_end, offset = transform
        for _src_start, _src_end, _dest_start, _dest_end, _offset in result:
            if _src_end >= src_start and src_end >= _src_start:
                log.info(f"Transform {src_start, src_end} overlaps {_src_start, _src_end}")
                # Transform overlaps range: re-queue portions that do not overlap
                if src_start < _src_start:
                    _len = _src_start - src_start - 1
                    log.info(f"Re-queueing before {src_start, src_start + _len}")
                    transforms_queue.append((src_start, src_start + _len, dest_start, dest_start + _len, offset))
                if src_end > _src_end:
                    _len = src_end - _src_end - 1
                    log.info(f"Re-queueing after {src_end - _len, src_end}")
                    transforms_queue.append((src_end - _len, src_end, dest_end - _len, dest_end, offset))
                break
        else:
            # Transform does not overlap any existing ranges: add to ranges
            result.append(transform)

    return list(sorted(result))


def merge_all_transforms(transforms_lst):
    ranges = []
    for transforms in transforms_lst:
        log.info(f"Merging: {transforms}")
        ranges = merge_transform(ranges, transforms)
        log.info(f"Ranges: {ranges}")
        log.info(f"")
    return ranges

    # ranges = [
    #     # range_start, range_end, range_offset
    #     (~sys.maxsize, sys.maxsize, 0)
    # ]
    # log.debug(f"Ranges: {ranges}")
    # for transform in transforms:
    #     log.debug(f"transform: {transform}")
    #     _ranges = ranges
    #     for dest_start, range_start, range_len in transform:
    #         range_end = range_start + range_len - 1
    #         range_offset = dest_start - range_start
    #         log.debug(f"  New range: {range_start}:{range_end} = {range_offset}")
    #         ranges = merge_range(ranges, range_start, range_end, range_offset)
    #     log.debug(f"Ranges: {ranges}\n")
    #
    # log.info(f"Merged {len(ranges)} ranges")
    # return ranges


def calculate(ranges, seed):
    for (src_start, src_end, _, _, offset) in ranges:
        if src_start <= seed <= src_end:
            return seed + offset
    return seed


def solve(ranges, seeds):
    result = sys.maxsize
    for seed in seeds:
        _result = calculate(ranges, seed)
        log.info(f"{seed} = {_result}")
        result = min(result, _result)
    return result


# def expand_seeds(seeds):
#     for seed_start, seed_range in grouper(seeds, 2):
#         log.info(f"{seed_start}:{seed_range}")
#         for i in range(seed_range):
#             yield seed_start + i


def main():
    args = parse_args()
    data = read_multilines(data_file_path_main(test=args.test))
    header = next(data)
    seeds = list(map(int, header[0].split("seeds: ", 1)[1].split(" ")))

    transforms_lst = []
    for lines in data:
        transforms = []
        for line in lines[1:]:
            dest_start, src_start, _len = map(int, line.split(" "))
            transform = (src_start, src_start + _len - 1, dest_start, dest_start + _len - 1, dest_start - src_start)
            transforms.append(transform)
        transforms_lst.append(list(sorted(transforms)))
    # print(transforms_lst)
    transforms_lst = transforms_lst[:2]
    ranges = merge_all_transforms(transforms_lst)
    log.info(f"Ranges: {ranges}")

    log.always("Part 1:")
    result = solve(ranges, seeds)
    log.always(result)

    # log.always("Part 2:")
    # result = solve(transforms, expand_seeds(seeds))
    # log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
