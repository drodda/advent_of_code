#!/usr/bin/env python3

import collections
import math
import sys
import traceback

from common.utils import *


SIGNAL_LOW = False
SIGNAL_HIGH = True
N = 1000
OUTPUT_NODE = "rx"


class SignalQueue:
    def __init__(self):
        self.pulses_low = 0
        self.pulses_high = 0
        self.queue = collections.deque()

    def push(self, dest, src, val):
        if val == SIGNAL_LOW:
            self.pulses_low += 1
        else:
            self.pulses_high += 1
        self.queue.append((dest, src, val))

    def reset(self):
        self.pulses_low = 0
        self.pulses_high = 0

    def items(self):
        while self.queue:
            yield self.queue.popleft()


class Module:
    def __init__(self, name, outputs, queue):
        self.name = name
        self.outputs = outputs
        self.inputs = []
        self.queue = queue

    def handle_signal(self, src_name, signal):
        raise NotImplemented

    def output(self, signal):
        log.debug(f"  {self.__class__.__name__} {self.name}: Sending {signal} to {self.outputs}")
        for name in self.outputs:
            self.queue.push(name, self.name, signal)

    def status(self):
        return ""

    def __str__(self):
        return f"{self.__class__.__name__}<{self.name}, {self.outputs}, {self.inputs}>"

    def __repr__(self):
        return str(self)


class BroadcastModule(Module):
    def handle_signal(self, src_name, signal):
        # Forward signal to all outputs
        self.output(signal)


class FlipFlopModule(Module):
    state = SIGNAL_LOW  # Off

    def handle_signal(self, src_name, signal):
        if signal == SIGNAL_LOW:
            self.state = not self.state
            self.output(self.state)

    def status(self):
        return f"{self.state}"


class ConjunctionModule(Module):
    def __init__(self, name, outputs, queue):
        super().__init__(name, outputs, queue)
        self.last_inputs = {}

    def handle_signal(self, src_name, signal):
        self.last_inputs[src_name] = signal
        self.output(not all([self.last_inputs.get(name) for name in self.inputs]))

    def status(self):
        return f"{self.last_inputs}"


MODULE_TYPES = {
    "%": FlipFlopModule,
    "&": ConjunctionModule,
}


def solve(lines):
    queue = SignalQueue()
    modules = {}
    for line in lines:
        module_type = line[0]
        name, outputs_str = line.strip("%&").split(" -> ")
        module_cls = MODULE_TYPES.get(module_type, BroadcastModule)
        outputs = tuple(outputs_str.split(", "))
        modules[name] = module_cls(name, outputs, queue)
    for name, module in modules.items():
        for output in module.outputs:
            if output in modules:
                modules[output].inputs.append(name)

    # Determine inputs to OUTPUT_NODE module
    watched_senders = [name for name, module in modules.items() if OUTPUT_NODE in module.outputs]
    if len(watched_senders) != 1:
        log.error(f"ERROR: {OUTPUT_NODE} is triggered by {watched_senders}")
        return None, None
    watched_sender_module = modules[watched_senders[0]]
    if not isinstance(watched_sender_module, ConjunctionModule):
        log.error(f"ERROR: {watched_sender_module.name} is {watched_sender_module.__class__.__name__} not {ConjunctionModule.__name__}")
        return None, None
    # Watch inputs to sender to OUTPUT_NODE module
    watched_inputs = {name: 0 for name in watched_sender_module.inputs}

    i = 0
    result_1 = None
    while result_1 is None or not all(watched_inputs.values()):
        i += 1
        queue.push("broadcaster", "button", SIGNAL_LOW)
        for dest_name, src_name, signal in queue.items():
            if i == N:
                # Check part1 end condition
                result_1 = queue.pulses_low * queue.pulses_high
            if watched_inputs and signal == SIGNAL_HIGH and watched_inputs.get(src_name) == 0:
                # Check part2 end condition
                watched_inputs[src_name] = i
            if dest_name in modules:
                module = modules[dest_name]
                log.debug(f"Processing signal: {signal} -> {dest_name}({module.status()}) (from {src_name})")
                module.handle_signal(src_name, signal)
        log.info(f"{i:8d}: Pulses = {queue.pulses_low} + {queue.pulses_high}")
    result_part2 = math.lcm(*watched_inputs.values())
    return result_1, result_part2


def main():
    args = parse_args()
    lines = read_lines(args.input, to_list=True)

    result_1, result_2 = solve(lines)
    log.always("Part 1:")
    log.always(result_1)

    log.always("Part 2:")
    log.always(result_2)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("Killed")
    except Exception:
        traceback.print_exc()
        sys.exit(-1)
