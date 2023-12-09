#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def solve(transforms, seed_ranges):
    for i, transform in enumerate(transforms):
        # TODO: This could be made more efficient by de-duplicating seed_ranges
        log.info(f"{i}: Processing: {transform}")
        log.info(f"{i}: Ranges = {seed_ranges}")
        _seed_ranges = []
        for seed_start, seed_len in seed_ranges:
            log.debug(f"  Mapping {seed_start}+{seed_len}")
            for dest_start, src_start, _range in transform:
                # Seed range (or part thereof) before transform mapping remains unchanged
                _len = min(seed_len, src_start - seed_start)
                if _len > 0:
                    log.debug(f"  > {seed_start}+{_len} (unchanged)")
                    _seed_ranges.append((seed_start, _len))
                    seed_start += _len
                    seed_len -= _len
                # Now seed_start > src_start if seed_len > 0
                # Range covered by this transform - apply transform mapping
                _len = min(seed_len, src_start + _range - seed_start)
                if _len > 0:
                    _seed_start = seed_start - src_start + dest_start
                    log.debug(f"  > {seed_start}+{_len} -> {_seed_start}+{_len} (mapped from {src_start}+{_range}->{dest_start})")
                    _seed_ranges.append((_seed_start, _len))
                    seed_start += _len
                    seed_len -= _len
            # Seed range (or part thereof) after all transforms remains unchanged
            if seed_len > 0:
                log.debug(f"  > {seed_start}+{seed_len} (unchanged)")
                _seed_ranges.append((seed_start, seed_len))
            log.debug(f"")
        seed_ranges = _seed_ranges
        # break
    return min([seed_start for seed_start, seed_len in seed_ranges])


def main():
    args = parse_args()
    data = read_multilines(data_file_path_main(test=args.test))
    header = next(data)
    seeds = list(map(int, header[0].split("seeds: ", 1)[1].split(" ")))

    transforms = []
    for lines in data:
        transform = list(sorted([
            list(map(int, line.split(" ")))
            for line in lines[1:]
        ], key=lambda lst: lst[1]))
        transforms.append(transform)

    log.always("Part 1:")
    seed_ranges = [(v, 1) for v in seeds]
    result = solve(transforms, seed_ranges)
    log.always(result)

    log.always("Part 2:")
    seed_ranges = grouper(seeds, 2, to_list=True)
    result = solve(transforms, seed_ranges)
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
