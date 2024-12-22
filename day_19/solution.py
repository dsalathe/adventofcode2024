"""
Advent of Code 2024 - Day 19
https://adventofcode.com/2024/day/19
"""
from functools import cache

def parse_input(input_data):
    """Parse the puzzle input."""
    lines = [line.strip() for line in input_data.split("\n") if line.strip()]
    patterns = tuple([p.strip() for p in lines[0].split(",")])
    words = lines[1:]
    return patterns, words

@cache
def count_combinations(word, patterns):
    if not word:
        return 1
    return sum(count_combinations(word[len(pattern):], patterns)
               for pattern in patterns if word.startswith(pattern))

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    patterns, words = data
    return sum(count_combinations(word, patterns) > 0 for word in words)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    patterns, words = data
    return sum(count_combinations(word, patterns) for word in words)

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
