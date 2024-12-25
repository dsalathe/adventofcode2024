"""
Advent of Code 2024 - Day 25
https://adventofcode.com/2024/day/25
"""

def get_heights(grid):
    return [col.index('.') for col in zip(*grid)]

def parse_input(input_data):
    locks, keys = [], []    
    for schematic in input_data.strip().split('\n\n'):
        grid = schematic.splitlines()
        if all(c == '#' for c in grid[0]):
            locks.append(get_heights(grid))
        elif all(c == '#' for c in grid[-1]):
            keys.append(get_heights(grid[::-1]))
    
    return locks, keys

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    locks, keys = data
    return sum(all(l + k <= 7 for l, k in zip(lock, key)) for lock in locks for key in keys)

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

if __name__ == "__main__":
    main()
