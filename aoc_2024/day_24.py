#!/usr/bin/env python3
import collections
import operator
import sys
import traceback

from common.utils import *


OPERATORS = {
    "AND": operator.iand,
    "OR": operator.ior,
    "XOR": operator.ixor,
}


def parse_input(args):
    values_lines, gate_lines = read_multilines(args.input)
    values = {}
    for values_line in values_lines:
        node, value_str = values_line.split(": ")
        values[node] = int(value_str)
    gates = []
    for gate_line in gate_lines:
        in1, operand, in2, _, output = gate_line.split(" ")
        in1, in2 = sorted([in1, in2])
        gates.append((in1, in2, operand, output))
    return values, gates


def solve_part1(values, gates):
    values = values.copy()
    # Identify gates that are solvable
    solvable = collections.deque()
    dependencies = collections.defaultdict(set)
    solved = set()
    for gate in gates:
        in1, in2, _, output = gate
        dependencies[in1].add(gate)
        dependencies[in2].add(gate)
        if in1 in values and in2 in values:
            solvable.append(gate)
    # Solve solvable gates
    while solvable:
        gate = solvable.popleft()
        in1, in2, operand, output = gate
        values[output] = OPERATORS[operand](values[in1], values[in2])
        solved.add(gate)
        # Identify new gates that are solvable
        for _gate in dependencies[output]:
            _in1, _in2, _, _output = _gate
            if _gate not in solved and _in1 in values and _in2 in values:
                solvable.append(_gate)
    # Calculate Z value bit-wise
    result = 0
    for node, value in values.items():
        if node.startswith("z") and value:
            index = int(node[1:])
            result += 1 << index
    return result


def find_gate(gates, in1, in2, operand):
    for gate in gates:
        if gate[:3] == [in1, in2, operand] or gate[:3] == [in2, in1, operand]:
            return gate
    return None


def find_output_gate(gates, output):
    for gate in gates:
        if gate[3] == output:
            return gate
    return None


def swap_gates(gate1, gate2):
    gate1[3], gate2[3] = gate2[3], gate1[3]


def solve_part2(gates):
    # Make gates mutable
    gates = [list(gate) for gate in gates]
    z_max = max([int(output[1:]) for *_, output in gates if output.startswith("z")])

    errors = set()
    while True:
        carry_gate = None
        for i in range(z_max):
            x = f"x{i:02d}"
            y = f"y{i:02d}"
            z = f"z{i:02d}"

            xy_xor_gate = find_gate(gates, x, y, "XOR")
            z_output_gate = find_output_gate(gates, z)
            if xy_xor_gate is None:
                log.error(f"No gate XOR {x, y}")
                return None
            if i == 0:
                if xy_xor_gate[3] != z:
                    # xy_xor_gate should output to z - is swapped
                    log.info(f"Swapped gates: {xy_xor_gate} and {z_output_gate}")
                    errors.add(xy_xor_gate[3])
                    errors.add(z_output_gate[3])
                    swap_gates(xy_xor_gate, z_output_gate)
                    break
                carry_gate = find_gate(gates, x, y, "AND")
                if carry_gate is None:
                    log.error(f"No gate AND {x, y}")
                    return None
            else:
                xy_and_gate = find_gate(gates, x, y, "AND")
                if xy_and_gate is None:
                    log.error(f"No gate AND {x, y}")
                    return None
                carry_xy_xor_gate = find_gate(gates, xy_xor_gate[3], carry_gate[3], 'XOR')
                if carry_xy_xor_gate is None:
                    log.info(f"Swapped gates: {xy_xor_gate} and {xy_and_gate}")
                    errors.add(xy_xor_gate[3])
                    errors.add(xy_and_gate[3])
                    swap_gates(xy_xor_gate, xy_and_gate)
                    break
                if carry_xy_xor_gate[3] != z:
                    # carry_xy_xor_gate should output to z - is swapped
                    log.info(f"Swapped gates: {carry_xy_xor_gate} and {z_output_gate}")
                    errors.add(carry_xy_xor_gate[3])
                    errors.add(z_output_gate[3])
                    swap_gates(carry_xy_xor_gate, z_output_gate)
                    break
                carry_xy_and_gate = find_gate(gates, xy_xor_gate[3], carry_gate[3], 'AND')
                carry_gate = find_gate(gates, xy_and_gate[3], carry_xy_and_gate[3], 'OR')
        else:
            # Loop finished - all gates work
            if carry_gate[3] != f"z{z_max:02d}":
                log.error(f"Final gate not connected to output: {carry_gate}")
            break
    return ",".join(sorted(errors))


def main():
    args = parse_args()
    values, gates = parse_input(args)

    log.always("Part 1:")
    result = solve_part1(values, gates)
    log.always(result)

    log.always("Part 2:")
    result = solve_part2(gates)
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
