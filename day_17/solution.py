"""
Advent of Code 2024 - Day 17
https://adventofcode.com/2024/day/17
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    lines = [line.strip() for line in input_data.split('\n') if line.strip()]
    
    registers = {'A': 0, 'B': 0, 'C': 0}
    for line in lines:
        if line.startswith('Register'):
            reg, value = line.split(':')
            reg = reg[-1]
            registers[reg] = int(value.strip())
        elif line.startswith('Program:'):
            program = [int(x) for x in line.split(':')[1].strip().split(',')]
            
    return registers, program

def run_program(a, b, c, program):
    output = []
    ip = 0

    def get_combo(op):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return a
        elif op == 5:
            return b
        elif op == 6:
            return c
        raise ValueError(f"Invalid combo operand: {op}")
    
    while ip < len(program):
        opcode, operand, combo = program[ip], program[ip + 1], get_combo(program[ip + 1])
            
        if opcode == 0:  # adv
            a >>= combo
        elif opcode == 1:  # bxl
            b ^= operand
        elif opcode == 2:  # bst
            b = combo % 8
        elif opcode == 3:  # jnz
            if a != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            b ^= c
        elif opcode == 5:  # out
            output.append(combo % 8)
        elif opcode == 6:  # bdv
            b = a >> combo
        elif opcode == 7:  # cdv
            c = a >> combo
            
        ip += 2
        
    return output

def search(a, b, c, program, length):
    if length == len(program) + 1:
        return a
        
    for bits in range(8):
        new_a = (a << 3) | bits
        if run_program(new_a, b, c, program) == program[len(program) - length:]:
            if result := search(new_a, b, c, program, length + 1):
                return result
                
    return None

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    registers, program = data
    output = run_program(registers['A'], registers['B'], registers['C'], program)
    return ','.join(str(x) for x in output)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    registers, program = data
    a = search(0, registers['B'], registers['C'], program, 1)
    assert run_program(a, registers['B'], registers['C'], program) == program
    return a

def main(input_file="input/input.txt"):
    with open(input_file) as f:
        input_data = f.read()
    
    data = parse_input(input_data)
    
    part1_solution = solve_part1(data)
    print(f"Part 1: {part1_solution}")
    
    part2_solution = solve_part2(data)
    print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()