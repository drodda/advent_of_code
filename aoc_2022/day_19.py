#!/usr/bin/env python3

import re
import sys
import traceback
from common.utils import *


RE_LINE = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."


# Upper limit on resources. Empirically chosen
RESOURCE_LIMIT = 50


def parse_input(test=False):
    lines = read_lines(input_file_path_main(test=test))
    _re = re.compile(RE_LINE)
    result = []
    for line in lines:
        m = _re.match(line)
        if not m:
            raise ValueError(f"Unable to parse line {line}")
        vals = list(map(int, m.groups()))
        result.append(vals)
    return result


def simulate(t_max, costs):
    ore_cost_ore, clay_cost_ore, obs_cost_ore, obs_cost_clay, geo_cost_ore, geo_cost_obs = costs
    ore_max = max([ore_cost_ore, clay_cost_ore, obs_cost_ore, geo_cost_ore])
    clay_max = obs_cost_clay
    obs_max = geo_cost_obs

    # Starting state: 1 ore
    states = {((0, 0, 0, 0), (1, 0, 0, 0)), }
    #
    explored = set()

    result = 0
    max_geo_robots = 0
    for t in reversed(range(t_max)):
        _states = set()
        log.info(f"{t}: {len(states)} states")
        for state in states:
            if state in explored:
                continue
            resources, robots = state
            ore, clay, obs, geo = resources
            ore_robots, clay_robots, obs_robots, geo_robots = robots
            max_geo_robots = max(max_geo_robots, geo_robots)

            # Increment resources
            _ore = min(ore + ore_robots, RESOURCE_LIMIT)
            _clay = min(clay + clay_robots, RESOURCE_LIMIT)
            _obs = min(obs + obs_robots, RESOURCE_LIMIT)
            geo += geo_robots
            result = max(result, geo)

            # Don't bother building in the last turn
            if t == 0:
                continue

            # Don't bother searching if there is no way to get as many geo robots as the best state
            if geo_robots + t < max_geo_robots:
                continue

            # If a geode robot can be built, always build one
            if ore >= geo_cost_ore and obs >= geo_cost_obs:
                _resources = (_ore - geo_cost_ore, _clay, _obs - geo_cost_obs, geo)
                _robots = (ore_robots, clay_robots, obs_robots, geo_robots + 1)
                _states.add((_resources, _robots))
            else:
                if ore >= ore_cost_ore and ore_robots < ore_max:
                    _resources = (_ore - ore_cost_ore, _clay, _obs, geo)
                    _robots = (ore_robots + 1, clay_robots, obs_robots, geo_robots)
                    _states.add((_resources, _robots))
                if ore >= clay_cost_ore and clay_robots < clay_max:
                    _resources = (_ore - clay_cost_ore, _clay, _obs, geo)
                    _robots = (ore_robots, clay_robots + 1, obs_robots, geo_robots)
                    _states.add((_resources, _robots))
                if ore >= obs_cost_ore and clay >= obs_cost_clay and obs_robots < obs_max:
                    _resources = (_ore - obs_cost_ore, _clay - obs_cost_clay, _obs, geo)
                    _robots = (ore_robots, clay_robots, obs_robots + 1, geo_robots)
                    _states.add((_resources, _robots))
                # And do nothing
                _resources = (_ore, _clay, _obs, geo)
                _states.add((_resources, robots))

        # Add newly explored states to explored
        explored.update(states)
        # Loop through new states
        states = _states

    return result

def solve_part1(data):
    result = 0
    for n, *vals in data:
        _result = simulate(24, vals)
        log.info(f"Blueprint {n}: {_result}")
        result += n * _result
    return result


def solve_part2(data):
    result = 1
    for n, *vals in data[:3]:
        _result = simulate(32, vals)
        log.info(f"Blueprint {n}: {_result}")
        result *= _result
    return result


def main():
    args = parse_args()
    data = parse_input(test=args.test)

    log.always("Part 1:")
    result = solve_part1(data)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(data[:3])
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
