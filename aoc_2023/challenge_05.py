#!/usr/bin/env python3

import sys
import traceback

from common.utils import *

# To merge a layer of transform:
# For existing transforms, if transform.dest in any new transform, apply transform
# Add new transforms where (any part of) transform.src not covered by existing transforms
# Order for convenience?



def merge_transform(ranges, transforms):
    # dest_start, src_start, _len = transform
    # src_end = src_start + _len - 1
    # dest_end = dest_start + _len - 1
    # offset = dest_start - src_start

    # Create ordered iterable of transforms
    transforms = iter(sorted(transforms, key=lambda l: l[1]))
    ranges = iter(ranges)

    def _merge_transform():
        # if not ranges:
        #     log.debug(f"  No ranges, range {(src_end, src_end + _len - 1, dest_start, dest_start + _len - 1)}")
        #     yield (src_end, src_end + _len - 1, dest_start, dest_start + _len - 1)
        #     return
        #
        # void_start = ~sys.maxsize

        # Apply transform to range:
        # If transform is None or range << transform, yield range
        # If range is None or transform << range yield transform
        # If range


        for range in ranges:
            _src_start, _src_end, _dest_start, _dest_end = range

            # # Yield new range before this range
            # if src_start < _src_start and src_end >= void_start and void_start < _src_start:
            #     new_range_start = max(src_start, void_start)
            #     new_range_end = min(src_end, _src_start - 1)
            #     log.debug(f"  Before existing range: {(new_range_start, new_range_end, new_range_start + offset, new_range_end + offset)}")
            #     yield (new_range_start, new_range_end, new_range_start + offset, new_range_end + offset)
            # void_start = _src_end + 1

            # Yield existing ranges modified by transform
            # Range before transform
            if _dest_start < src_start:
                range_len = _dest_start - min(_dest_end, src_start - 1)
                log.debug(
                    f"  Range before transform: {(_src_start, _src_start + range_len, _dest_start, _dest_start + range_len)}")
                yield (_src_start, _src_start + range_len, _dest_start, _dest_start + range_len)
                # Trim range that is before transform
                _src_start += range_len + 1
                _dest_start += range_len + 1

            # Range overlapping transform
            if _dest_end >= src_start:
                range_len = _dest_start - min(_dest_end, src_end)
                yield (_src_start, _src_start + range_len, _dest_start + offset, _dest_start + range_len + offset)
                # Trim range that is before transform
                _src_start += range_len + 1
                _dest_start += range_len + 1

            # Range after transform
            if _dest_start <= _dest_end:
                range_len = _dest_end - _dest_start
                yield (_src_start, _src_end, _dest_start, _dest_end)

            # Yield new range(s) from transform that are not covered by existing ranges


        # # Yield new range after last range
        # _src_start, _src_end, _dest_start, _dest_end = ranges[-1]
        # if src_end < _src_end:
        #     range_len = src_end - _src_end - 1
        #     yield (max(src_end - range_len, src_start), src_end, min(dest_end + range_len, dest_start), dest_end)

    return list(sorted(_merge_transform()))


def merge_transforms(transforms):
    ranges = []
    for transform in transforms:
        print(transform)
        for _transform in transform:
            ranges = merge_transform(ranges, _transform)
            log.info(f"Transform {_transform} produces Ranges: {ranges}")
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
#
#
# def calculate(ranges, seed):
#     for (range_start, range_end, range_offset) in ranges:
#         if range_start <= seed <= range_end:
#             return seed + range_offset
#     raise ValueError(f"Ranges does not cover value {seed}")
#
#
# def solve(ranges, seeds):
#     result = sys.maxsize
#     for seed in seeds:
#         _result = calculate(ranges, seed)
#         log.info(f"{seed} = {_result}")
#         result = min(result, _result)
#     return result


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

    transforms = []
    for lines in data:
        transform = [
            list(map(int, line.split(" ")))
            for line in lines[1:]
        ]
        transforms.append(transform)
    transforms = transforms[:1]
    print(transforms)

    # transforms = transforms[:2]
    # for transform in transforms:
    #     transform = sorted(transform, key=lambda d: d[1])
    #     for i in range(1, len(transform)):
    #         if transform[i][1] != (transform[i-1][1] + transform[i-1][2]):
    #             print(f"Transform {i} {transform[i][1]} vs {transform[i-1][1]} + {transform[i-1][2]} is not contigeous: {transform}")



    ranges = merge_transforms(transforms)
    # log.info(f"Ranges: {ranges}")
    #
    # log.always("Part 1:")
    # result = solve(ranges, seeds)
    # log.always(result)
    #
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
