"""
Advent of Code 2024 - Day 24
https://adventofcode.com/2024/day/24
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class _Gate:
    type: str
    inputs: frozenset

def Gate(type, in1, in2):
    return _Gate(type, frozenset((in1, in2)))

def parse_input(input_data):
    sections = input_data.split("\n\n")
    wire_values = {wire.strip(): int(value) for wire, value in [line.split(": ") for line in sections[0].splitlines()]}
    gates = {
        Gate(gate_type, in1.strip(), in2.strip()) : output
        for in1, gate_type, in2, _, output in [line.split() for line in sections[1].splitlines()]
    }
    return wire_values, gates

def evaluate_gate(gate_type, val1, val2):
    return {
        'AND': int(val1 and val2),
        'OR': int(val1 or val2),
        'XOR': int(val1 != val2)
    }[gate_type]

def simulate_circuit(wire_values, gates):
    values = wire_values.copy()
    gates_to_evaluate = gates.keys()
    
    while gates_to_evaluate:
        processed_gates = set()
        for gate in gates_to_evaluate:
            if gate.inputs.issubset(values):
                result = evaluate_gate(gate.type, *[values[input] for input in gate.inputs])
                values[gates[gate]] = result
                processed_gates.add(gate)

        gates_to_evaluate -= processed_gates    
    return values

def get_z_value(wire_values):
    z_wires = [(wire, value) for wire, value in wire_values.items() if wire.startswith('z')]
    binary = ''.join(str(value) for _, value in sorted(z_wires, reverse=True))
    return int(binary, 2)    

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    wire_values, gates = data
    final_values = simulate_circuit(wire_values, gates)
    return get_z_value(final_values)

def find_swapped_wires(gates, ideal_gate):
    for gate in gates:
        if gate.type == ideal_gate.type and (ideal_gate.inputs & gate.inputs):
            # Mutually exclusive
            return gate.inputs ^ ideal_gate.inputs
    return None

def swap_bits(s1, s2, b1, b2, b3):
    return (s2 if b1 == s1 else (s1 if b1 == s2 else b1),
            s2 if b2 == s1 else (s1 if b2 == s2 else b2),
            s2 if b3 == s1 else (s1 if b3 == s2 else b3))

def update_gates(gates, s1, s2):
    return {
        gate: (s2 if output == s1 else (s1 if output == s2 else output))
        for gate, output in gates.items()
    }

def process_bit_position(gates, xor_output, and_output, carry):
    swapped_wires = []

    def handle_failed_lookup(ideal_gate): 
            s1, s2 = find_swapped_wires(gates, ideal_gate)
            swapped_wires.extend([s1, s2])
            return s1, s2
    
    and_gate = Gate("AND", xor_output, carry)
    if and_gate not in gates:
        s1, s2 = handle_failed_lookup(and_gate)
        gates = update_gates(gates, s1, s2)
        xor_output, carry, and_output = swap_bits(s1, s2, xor_output, carry, and_output)
    carry_chain = gates[Gate("AND", xor_output, carry)]

    or_gate = Gate("OR", carry_chain, and_output)
    if or_gate not in gates:
        s1, s2 = handle_failed_lookup(or_gate)
        gates = update_gates(gates, s1, s2)
        carry_chain, and_output, carry = swap_bits(s1, s2, carry_chain, and_output, carry)
    carry = gates[Gate("OR", carry_chain, and_output)]
    
    return swapped_wires, gates, carry

def solve_part2(data):
    """Solve part 2 of the puzzle by finding swapped gate outputs."""
    wire_values, gates = data
    x_wires = sorted([wire for wire in wire_values if wire.startswith('x')])
    y_wires = sorted([wire for wire in wire_values if wire.startswith('y')])
    
    swapped_wires = []
    carry = gates[Gate("AND", x_wires[0], y_wires[0])]

    for x_wire, y_wire in zip(x_wires[1:], y_wires[1:]):
        xor_output=gates[Gate("XOR", x_wire, y_wire)]
        and_output=gates[Gate("AND", x_wire, y_wire)]

        new_swaps, gates, carry = process_bit_position(gates, xor_output, and_output, carry)
        swapped_wires.extend(new_swaps)
    
    return ','.join(sorted(swapped_wires))

def main(input_file="input/input.txt"):
    """Main function to run the solution."""
    # Read input
    with open(input_file) as f:
        input_data = f.read()
    
    data = parse_input(input_data)
    part1_solution = solve_part1(data)
    print(f"\nPart 1: {part1_solution}")
    
    part2_solution = solve_part2(data)
    print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()