#!/usr/bin/env python3
import traceback
import queue

from utils import *

import intcode_vm
from intcode_vm import *

# Disable verbose logging from intcode_vm
intcode_vm.log_verbose = log_never
intcode_vm.log_debug = log_never


PHASES_LEN = 5


def run_simulation(data, phases):
    vms = []
    queues = [queue.Queue() for i in range(len(phases) + 1)]
    for i, phase in enumerate(phases):
        queues[i].put(phase)
    # Load initial power
    queues[0].put(0)
    for i, phase in enumerate(phases):
        vm = VMThread(data, input_queue=queues[i], output_queue=queues[i+1], tid=i)
        vms.append(vm)
    for vm in vms:
        vm.start()
    for vm in vms:
        vm.join()
    if queues[-1].empty():
        log_error(f"Warning: No output from from {phases}")
        return None
    return queues[-1].get()


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

        phase_permutations = itertools.permutations(range(PHASES_LEN))
        result_max = None
        result_phases = None
        for phases in phase_permutations:
            log_debug(phases)
            result = run_simulation(data, phases)
            if result_max is None or result > result_max:
                result_max = result
                result_phases = phases
        log_always(f"{result_max} from phases {result_phases}")


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        log_always("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
