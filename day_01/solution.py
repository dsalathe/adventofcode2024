"""
Advent of Code 2024 - Day 1
https://adventofcode.com/2024/day/1
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]

def to_lists(pairs):
    return list(zip(*[map(int, pair.split()) for pair in pairs]))

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    l1, l2 = to_lists(data)
    l1s, l2s = sorted(l1), sorted(l2)
    return sum(abs(e1 - e2) for (e1, e2) in zip(l1s, l2s))

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    from collections import Counter
    l1, l2 = to_lists(data)
    s1, s2 = Counter(l1), Counter(l2)
    return sum([s2[e] * e * s1[e] for e in s1.keys()])

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
