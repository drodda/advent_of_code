#!/usr/bin/env python3

import re
import sys
import traceback

from common.utils import *


RE = re.compile(r"(\S+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")


def parse_input(lines):
    result = {}
    for line in lines:
        m = RE.match(line)
        if m:
            name, *vals = m.groups()
            result[name] = list(map(int, vals))
        else:
            log.error(f"Bad line: {line}")
    return result


def calculate_distance(t, speed, fly_time, rest_time):
    n, r = divmod(t, fly_time + rest_time)
    result = speed * (n * fly_time + min(fly_time, r))
    return result


def simulate_part2(speeds, t):
    all_names = tuple([name for name in speeds.keys()])
    points = {name: 0 for name in all_names}
    positions = {name: 0 for name in all_names}
    winners = list(all_names)
    winning_distance = 0
    for i in range(t):
        for name, (speed, fly_time, rest_time) in speeds.items():
            _, r = divmod(i, fly_time + rest_time)
            if r < fly_time:
                positions[name] += speed
                if positions[name] > winning_distance:
                    winning_distance = positions[name]
                    winners = [name]
                elif positions[name] == winning_distance:
                    winners.append(name)
        # Award points to winners
        for name in winners:
            points[name] += 1
        log.debug(f"{i + 1}: {positions}, Points {points}, Winner {winners} @ {winning_distance}")
    return points


def main():
    args = parse_args()
    lines = read_lines(data_file_path_main(test=args.test), to_list=True)
    speeds = parse_input(lines)
    t = 1000 if args.test else 2503

    log.always("Part 1")
    result = 0
    for name, (speed, fly_time, rest_time) in speeds.items():
        d = calculate_distance(t, speed, fly_time, rest_time)
        log.debug(f"{name}: {d}")
        result = max(result, d)
    log.always(result)

    log.always("Part 2")
    points = simulate_part2(speeds, t)
    result = max(points.values())
    log.always(result)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
