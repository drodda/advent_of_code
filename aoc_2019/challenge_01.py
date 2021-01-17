#!/usr/bin/env python3

import traceback

from utils import *


def calculate_fuel_mass(mass):
    return int(mass / 3) - 2


def calculate_fuel_masses(mass):
    fuel_basic = calculate_fuel_mass(mass)
    fuel_recursive = 0
    fuel_mass = fuel_basic
    print_verbose(f"Mass {mass}:")
    while fuel_mass > 0:
        print_verbose(f"  {fuel_mass}")
        fuel_recursive += fuel_mass
        fuel_mass = calculate_fuel_mass(fuel_mass)
    return fuel_basic, fuel_recursive


###############################################################################


def main():
    args = parse_args()
    data_file = data_file_path_main(test=args.test)
    data = read_list_int(data_file)

    result_basic = 0
    result_recursive = 0
    for mass in data:
        fuel_basic,  fuel_recursive = calculate_fuel_masses(mass)
        result_basic += fuel_basic
        result_recursive += fuel_recursive
        print_debug(f"Mass: {mass} Fuel Basic {fuel_basic} Fuel Recursive {fuel_recursive}")

    print("Part 1")
    print(result_basic)
    print("Part 2")
    print(result_recursive)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
