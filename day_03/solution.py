"""
Advent of Code 2024 - Day 3
https://adventofcode.com/2024/day/3
"""

import re


def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]


def calculate_multiplications(text):
    pattern = r'mul\((\d+),(\d+)\)'
    matches = re.finditer(pattern, text)
    
    total_sum = 0
    for match in matches:
        n1 = int(match.group(1))
        n2 = int(match.group(2))
        product = n1 * n2
        total_sum += product
    
    return total_sum

def calculate_multiplications2(text, initial_state=True):
    mul_pattern = r'mul\((\d+),(\d+)\)'
    control_pattern = r'do\(\)|don\'t\(\)'
    
    mul_matches = [(m.start(), int(m.group(1)), int(m.group(2))) 
                  for m in re.finditer(mul_pattern, text)]
    
    control_matches = []
    for m in re.finditer(control_pattern, text):
        ctrl_type = 'do' if m.group(0) == 'do()' else "don't"
        control_matches.append((m.start(), ctrl_type))
    
    enabled = initial_state
    total_sum = 0
    final_state = enabled 
    
    all_events = []
    for pos, n1, n2 in mul_matches:
        all_events.append((pos, 'mul', (n1, n2)))
    for pos, ctrl_type in control_matches:
        all_events.append((pos, 'control', ctrl_type))
    
    all_events.sort()
    
    for _, event_type, data in all_events:
        if event_type == 'control':
            enabled = (data == 'do')
            final_state = enabled
        elif event_type == 'mul' and enabled:
            n1, n2 = data
            total_sum += n1 * n2
    
    return total_sum, final_state

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    totals = map(calculate_multiplications, data)
    return sum(totals)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    current_state = True  # Start enabled
    total = 0
    
    for line in data:
        line_sum, current_state = calculate_multiplications2(line, current_state)
        total += line_sum
    
    return total

def main(input_file="input/input.txt"):
    """Main function to run the solution."""
    # Read input
    with open(input_file) as f:
        input_data = f.read()
    
    # Parse input
    data = parse_input(input_data)
    
    # Solve parts
    part1_solution = solve_part1(data)
    print(f"Part 1: {part1_solution}")
    
    part2_solution = solve_part2(data)
    print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()
