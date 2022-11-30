#!/usr/bin/env python3
import itertools
import sys
import traceback
import re
import networkx as nx

from common.utils import *
from intcode_vm import *


OPPOSITE_DIRS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


# Items that should not be picked up
BAD_ITEMS = ['molten lava', 'escape pod', 'giant electromagnet', 'photons', 'infinite loop']
# Name of checkpoint node
CHECKPOINT_NAME = "Security Checkpoint"
# Regex for result
RE_RESULT = r"You should be able to get in by typing (?P<result>\d+) on the keypad at the main airlock"


class AsciiVM(VM):
    def __init__(self, mem, to_stdout=False):
        super().__init__(mem, output_queue="")
        self.to_stdout = to_stdout

    def _output(self, item):
        if self.to_stdout:
            print(chr(item), end="")
        else:
            self.output += chr(item)

    def read(self, clear=True):
        result = self.output
        if clear:
            self.output = ""
        return result

    def send(self, s):
        for c in s + "\n":
            self.input.put(ord(c))


def play_manual(data):
    vm = AsciiVM(data, to_stdout=True)
    try:
        while True:
            vm.run_until_input()
            print("> ", end="")
            line = input()
            vm.send(line)
    except (KeyboardInterrupt, EOFError):
        pass


def parse_output(output):
    parts = [item.split("\n") for item in output.strip().split("\n\n")]
    name = parts[0][0].strip(" =")
    description = parts[0][1]
    dirs = []
    items = []
    for lines in parts[1:]:
        # Strip leading "- " from values
        values = [line.lstrip("- ") for line in lines[1:]]
        if lines[0] == "Doors here lead:":
            dirs = values
        elif lines[0] == "Items here:":
            items = values

    return name, description, dirs, items


def calculate_next_direction(g, current_node, checkpoint_unlocked=False):
    destination = None
    path_length = None

    for _name, _path in nx.single_source_shortest_path(g, current_node).items():
        # Exclude explored destinations
        if g.nodes[_name]['explored']:
            continue
        # Ignore destinations via checkpoint unless checkpoint is unlocked
        if _path[-2] == CHECKPOINT_NAME and not checkpoint_unlocked:
            log.debug(f"  Skipping {_path}")
            continue
        # Trim current node from _path
        _path = _path[1:]
        _path_length = len(_path)
        _destination = _path[0]
        log.debug(f"  Can explore: {_name} via {_destination} for {_path_length}")
        # Find destination with shortest path
        if path_length is None or _path_length < path_length:
            destination = _destination
            path_length = _path_length
    log.info(f"  Exploring: {destination}")

    if destination is not None:
        return destination

    return None


def all_combinations(items):
    for i in range(0, len(items) + 1):
        for combination in itertools.combinations(items, i):
            yield combination


def brute_force_checkpoint(vm, _dir, all_items):
    log.info(f"Brute forcing items required to pass {CHECKPOINT_NAME}")
    # Brute force all combinations of items
    for items_keep in all_combinations(all_items):
        log.info(f"Trying: {items_keep}")
        # Collect items required
        for item in items_keep:
            vm.send(f"take {item}")
            vm.run_until_input()
        log.debug("################################")
        log.debug(vm.read(clear=True))
        log.debug("################################")

        # Try to proceed
        vm.send(_dir)
        try:
            vm.run_until_input()
        except StopIteration:
            # Succeeded!
            output = vm.read(clear=True)
            log.debug("################################")
            log.debug(output)
            log.debug("################################")
            m = re.search(RE_RESULT, output)
            if m:
                result = m.group("result")
                return result
        output = vm.read(clear=True)
        log.debug("################################")
        log.debug(output)
        log.debug("################################")
        if "Alert! Droids on this ship are heavier than the detected value" in output:
            log.info("Failed: too light")
        elif "Alert! Droids on this ship are lighter than the detected value!" in output:
            log.info("Failed: too heavy")
        else:
            log.info("Error - expected failure did not occur")
            break
        # Drop all items
        for item in items_keep:
            vm.send(f"drop {item}")
            vm.run_until_input()
        log.debug("################################")
        log.debug(vm.read(clear=True))
        log.debug("################################")

    return None


def solve(data):
    vm = AsciiVM(data)

    g = nx.DiGraph()
    _current_node = "start"
    g.add_node(_current_node, explored=False)
    inventory = set()
    checkpoint_unlocked = False
    while True:
        vm.run_until_input()
        log.debug("################################")
        log.debug(vm.read(clear=False))
        log.debug("################################")
        current_node, description, dirs, items = parse_output(vm.read(clear=True))
        nx.relabel_nodes(g, {_current_node: current_node}, copy=False)
        log.info(f"Entering: {current_node} ({'explored' if g.nodes[current_node]['explored'] else 'new'})")
        g.nodes[current_node]['explored'] = True

        # Take all items from current node
        for item in items:
            if item in BAD_ITEMS:
                log.info(f"Skipping Item: {item}")
            else:
                log.info(f"Collecting Item: {item}")
                vm.send(f"take {item}")
                vm.run_until_input()
                log.debug("################################")
                log.debug(vm.read(clear=True))
                log.debug("################################")
                inventory.add(item)

        # Create new nodes for all directions
        # if current_node in ["Security Checkpoint", "Pressure-Sensitive Floor", "Warp Drive Maintenance"]:
        #     trace()
        known_edges = [data["dir"] for _, _, data in g.edges(current_node, data=True)]
        for _dir in dirs:
            if _dir in known_edges:
                continue
            new_node_name = f"unexplored<{current_node}:{_dir}>"
            g.add_node(new_node_name, explored=False)
            g.add_edge(current_node, new_node_name, dir=_dir)
            g.add_edge(new_node_name, current_node, dir=OPPOSITE_DIRS[_dir])

        destination = calculate_next_direction(g, current_node, checkpoint_unlocked)

        if destination is None:
            # No unexplored destinations
            if current_node == CHECKPOINT_NAME:
                checkpoint_unlocked = True
                # At checkpoint: Work out items required to be carried to proceed
                # Drop all items
                for item in inventory:
                    log.info(f"Dropping Item: {item}")
                    vm.send(f"drop {item}")
                    vm.run_until_input()
                    log.debug("################################")
                    log.debug(vm.read(clear=True))
                    log.debug("################################")

                # Find new destination now that checkpoint is unlcoked
                destination = calculate_next_direction(g, current_node, checkpoint_unlocked)
                _dir = g.get_edge_data(current_node, destination)["dir"]
                result = brute_force_checkpoint(vm, _dir, inventory)
                return result
            else:
                # Move to checkpoint. Assume it has been found already
                _path = nx.single_source_shortest_path(g, current_node).get(CHECKPOINT_NAME)
                if _path is None:
                    raise RuntimeError(f"No path to {CHECKPOINT_NAME}")
                destination = _path[1]

        _dir = g.get_edge_data(current_node, destination)["dir"]
        log.info(f"Going {_dir} to {destination}")
        vm.send(_dir)
        _current_node = destination


def main():
    args = parse_args()
    data = read_csv_int(data_file_path_main(test=False), to_list=True)

    if args.test:
        play_manual(data)
        return

    log.always("Part 1")
    result = solve(data)
    log.always("")
    log.always("Result:")
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
