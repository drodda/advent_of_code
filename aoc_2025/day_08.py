#!/usr/bin/env python3
import collections
import math
import sys
import traceback

from common.utils import *


def parse_input(args):
    data = []
    for line in read_lines(args.input):
        data.append(list(map(int, line.split(","))))
    return data


def calculate_distance(coords_1, coords_2):
    x1, y1, z1 = coords_1
    x2, y2, z2 = coords_2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def solve(data, n):
    distances = {}
    for node_1, coord_1 in enumerate(data):
        for node_2 in range(node_1 + 1, len(data)):
            coord_2 = data[node_2]
            dist = calculate_distance(coord_1, coord_2)
            distances[(node_1, node_2)] = dist

    result_1 = None
    result_2 = None
    circuits = {}
    circuit_owners = {}
    for i, (node_1, node_2) in enumerate(sorted(distances, key=distances.get)):
        # Create a new circuit containing all the nodes linked to node_1 and node_2
        circuit = {node_1, node_2}
        circuit.update(circuits.pop(circuit_owners.get(node_1), set()))
        circuit.update(circuits.pop(circuit_owners.get(node_2), set()))
        circuit_owner = min(circuit)
        circuits[circuit_owner] = circuit
        for node in circuit:
            circuit_owners[node] = circuit_owner

        # After n connections, calculate size of largest circuits
        if (i + 1) == n:
            circuit_sizes = sorted(map(len, circuits.values()), reverse=True)
            result_1 = math.prod(circuit_sizes[:3])

        # Identify when all nodes are in a single circuit
        if len(circuits.get(0, [])) == len(data):
            result_2 = data[node_1][0] * data[node_2][0]

        # Exit when both parts re solved!
        if result_1 is not None and result_2 is not None:
            break

    return result_1, result_2


def main():
    args = parse_args()
    data = parse_input(args)

    n = 10 if args.test else 1000

    result_1, result_2 = solve(data, n)

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
