#!/usr/bin/env python3

import sys
import traceback
import math
import numpy as np

from common.utils import *


def next_time(time_now, time_start):
    """ Return the next multiple of time_start after time_now """
    return math.ceil(time_now/time_start) * time_start


def main():
    args = parse_args()

    data_file = input_file_path_main(test=args.test)
    data = read_lines(data_file, to_list=True)

    time_now = int(data[0])
    times_full = [int(i) if i.isnumeric() else i for i in data[1].split(",")]
    log.verbose(times_full)
    times = [i for i in times_full if i != "x"]

    log.always("Part 1")
    times_next = [next_time(time_now, t) for t in times]
    time_next = min(times_next)
    i = times_next.index(time_next)
    log.debug(f"Now: {time_now}, next: {time_next} ({i}: {times[i]})")
    part1_result = times[i] * (time_next - time_now)
    log.always(part1_result)

    log.always("Part 2")
    # Accumulator
    time_next = 0
    # LCM of all times encountered times so far
    lcm = 1
    for i, t in enumerate(times_full):
        if t != "x":
            # Increment accumulator by LCM until this value meets requirements
            while (time_next + i) % t != 0:
                time_next += lcm
            # Calculate new LCM as LCM of all numbers encountered so far
            lcm = np.lcm(lcm, t)
            # Debug: print times encountered so far
            if args.verbose:
                for _i in range(i+1):
                    _t = times_full[_i]
                    if _t != "x":
                        log.verbose(f"  {_i}: {time_next} % {_t} == {time_next % _t}  ({(time_next * -1) % _t})")
                log.verbose()
    log.always(time_next)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
