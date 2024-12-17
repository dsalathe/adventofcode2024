"""
Advent of Code 2024 - Day 2
https://adventofcode.com/2024/day/2
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]

def list_list_int(line):
    return list(map(int, line.split()))

def is_safe(report):
    direction = report[1] - report[0]
    if direction == 0:
        return False
    for (n1, n2) in zip(report, report[1:]):
        e1, e2 = (n1, n2) if direction > 0 else (n2, n1)
        if not (e2 > e1 and e1 + 4 > e2):
            return False
    return True

def is_safe2(report):
    if is_safe(report):
        return True
    for i in range(len(report)):
        subreport = report[:i] + report[i+1:]
        if is_safe(subreport):
            return True
    return False

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    reports = list(map(list_list_int, data))
    total = len([report for report in reports if is_safe(report)])
    return total

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    reports = list(map(list_list_int, data))
    total = len([report for report in reports if is_safe2(report)])
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
