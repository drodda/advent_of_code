#!/usr/bin/env python3

import sys
import traceback

from common.utils import *


def calculate_fuel_mass(mass):
    return int(mass / 3) - 2


def calculate_fuel_masses(mass):
    fuel_basic = calculate_fuel_mass(mass)
    fuel_recursive = 0
    fuel_mass = fuel_basic
    log.verbose(f"Mass {mass}:")
    while fuel_mass > 0:
        log.verbose(f"  {fuel_mass}")
        fuel_recursive += fuel_mass
        fuel_mass = calculate_fuel_mass(fuel_mass)
    return fuel_basic, fuel_recursive


###############################################################################


def main():
    args = parse_args()
    data_file = args.input
    data = read_list_int(data_file)

    result_basic = 0
    result_recursive = 0
    for mass in data:
        fuel_basic,  fuel_recursive = calculate_fuel_masses(mass)
        result_basic += fuel_basic
        result_recursive += fuel_recursive
        log.debug(f"Mass: {mass} Fuel Basic {fuel_basic} Fuel Recursive {fuel_recursive}")

    log.always("Part 1")
    log.always(result_basic)
    log.always("Part 2")
    log.always(result_recursive)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log.always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
