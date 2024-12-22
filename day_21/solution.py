"""
Advent of Code 2024 - Day 22
https://adventofcode.com/2024/day/22

Important observations:
1. we need to move as less as possible. So doing >>^^ would always be better
   than interleaving the moves like >^>^, because pressing the same key twice avoids moving.
   => This means we should only test full horizontal then vertical mvoes or vice versa.
2. Solving one layer at a time is not enough, because the output shortest path of some layer
   might not be the optimal input for the next layer.
3. Solving one character at a time across each layer is the key and works fine, because
   every layer needs to be reset to 'A' (for pushing the button) making each character computation independent.
4. Because each code ends with 'A' we can simplify a bit how to handle each layer.
"""

from functools import cache

def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]

NUMBER_PAD = {
    char: (x, y)
    for y, row in enumerate([
        ["7" , "8", "9"],
        ["4" , "5", "6"],
        ["1" , "2", "3"],
        [None, "0", "A"]
    ])
    for x, char in enumerate(row)
    if char is not None
}

DIR_PAD = {
    char: (x, y)
    for y, row in enumerate([
        [None, "^", "A"],
        ["<" , "v", ">"]
    ])
    for x, char in enumerate(row)
    if char is not None
}
A = "A"

def get_position(code, is_numeric):
    return NUMBER_PAD[code] if is_numeric else DIR_PAD[code]

@cache
def shortest_path(start_symbol, end_symbol, layer, is_numeric=False):
    if layer == 0:
        return 1
    
    path = lambda start, end: shortest_path(start, end, layer - 1)
    start = get_position(start_symbol, is_numeric)
    end = get_position(end_symbol, is_numeric)

    dist_v = abs(end[1] - start[1])
    dist_h = abs(end[0] - start[0])
    v = "^" if end[1] < start[1] else "v" if end[1] > start[1] else None
    h = "<" if end[0] < start[0] else ">" if end[0] > start[0] else None

    if dist_v == dist_h == 0:
        return path(A, A)
    if dist_v == 0:
        return (path(A, h) + 
                path(h, h) * (dist_h - 1) + 
                path(h, A))
    if dist_h == 0:
        return (path(A, v) + 
                path(v, v) * (dist_v - 1) + 
                path(v, A))

    horizontal_first = (
        path(A, h) + 
        path(h, h) * (dist_h - 1) +
        path(h, v) + 
        path(v, v) * (dist_v - 1) + 
        path(v, A)
    )

    vertical_first = (
        path(A, v) + 
        path(v, v) * (dist_v - 1) +
        path(v, h) + 
        path(h, h) * (dist_h - 1) + 
        path(h, A)
    )

    if is_numeric:
        force_horizontal_first = start[0] == 0 and end[1] == 3
        force_vertical_first = end[0] == 0 and start[1] == 3
    else:
        force_horizontal_first = start[0] == 0
        force_vertical_first = end[0] == 0

    if force_horizontal_first:
        return horizontal_first
    
    if force_vertical_first:
        return vertical_first
        
    return min(horizontal_first, vertical_first)
    
def solve(data, total_layers):
    total_complexity = 0
    
    for code in data:
        numeric_value = int(code[:-1])
        total_steps = sum(shortest_path(start_symbol, end_symbol, total_layers, is_numeric=True) 
                          for start_symbol, end_symbol in zip("A" + code, code))
            
        complexity = numeric_value * total_steps
        total_complexity += complexity
        
    return total_complexity

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    return solve(data, 3)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    return solve(data, 26)

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
    if part2_solution is not None:
        print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()