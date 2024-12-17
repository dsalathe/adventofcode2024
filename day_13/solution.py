"""
Advent of Code 2024 - Day 13
https://adventofcode.com/2024/day/13
"""

def parse_input(input_data):
    def parse_coords(line):
        x, y = line.split(': ')[1].split(', ')
        x_val = int(x.split('+' if '+' in x else '=')[1])
        y_val = int(y.split('+' if '+' in y else '=')[1])
        return [x_val, y_val]
        
    return [tuple(parse_coords(line) for line in machine.strip().splitlines())
            for machine in input_data.strip().split('\n\n')]

def cramer(coefficients):
    """
    Solve system of equations using Cramer's Rule
    [a1, b1, c1, a2, b2, c2] represents:
    a1x + b1y = c1
    a2x + b2y = c2
    see https://en.wikipedia.org/wiki/Cramer%27s_rule#Explicit_formulas_for_small_systems
    """
    a1, b1, c1, a2, b2, c2 = coefficients
    denom = a1 * b2 - b1 * a2
        
    dx = c1 * b2 - b1 * c2
    dy = a1 * c2 - a2 * c1
    
    if dx % denom != 0 or dy % denom != 0:
        return None
        
    return (dx // denom, dy // denom)

def solve_part1(data):
    total_tokens = 0
    for machine in data:
        button_a, button_b, prize = machine
        
        coefficients = [
            button_a[0], button_b[0], prize[0], # x
            button_a[1], button_b[1], prize[1]  # y
        ]
        
        solution = cramer(coefficients)
        if solution:
            a, b = solution
            total_tokens += (3*a + b)
    
    return total_tokens

def solve_part2(data):
    offset = 10_000_000_000_000
    for machine in data:
        prize = machine[2]
        prize[0] += offset
        prize[1] += offset

    return solve_part1(data)

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
