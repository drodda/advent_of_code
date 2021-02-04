#!/usr/bin/env python3
import traceback

from utils import *

import challenge_05
from challenge_05 import VM
# Disable verbose logging from challenge_05
challenge_05.log_verbose = log_never
challenge_05.log_debug = log_never


PHASES_LEN = 5


def run_simulation(data, phases):
    power = 0
    for i, phase in enumerate(phases):
        input_values = [phase, power]
        vm = VM(data, input_values=input_values)
        vm.run()
        if len(vm.output) != 1:
            log_error(f"Warning: No output from step {i} from {phases}")
            return None
        power = vm.output[0]
        log_debug(f"Step {i} input {input_values} output {power}")
    return power


def data_str(data):
    if len(data) < 6:
        return " ".join(map(str, data))
    return "{} ... {}".format(" ".join(map(str, data[:3])), " ".join(map(str, data[-3:])))


def main():
    args = parse_args()

    lines = read_lines(data_file_path_main(test=args.test))
    for i, line in enumerate(lines):
        data = list(map(int, line.split(",")))
        log_always(f"{i}: {data_str(data)}")

        # phases = [4, 3, 2, 1, 0]
        # result = run_simulation(data, phases)
        # log_always(result)
        # return

        phase_permutations = itertools.permutations(range(PHASES_LEN))
        result_max = None
        result_phases = None
        for phases in phase_permutations:
            log_debug(phases)
            result = run_simulation(data, phases)
            if result_max is None or result > result_max:
                result_max = result
                result_phases = phases
        log_always(f"{result_max} ({result_phases})")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
