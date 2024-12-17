"""
Advent of Code 2024 - Day 11
https://adventofcode.com/2024/day/11
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    return [list(map(int, line.split())) for line in input_data.split('\n') if line.strip()][0]


def transform(stone):
    if stone == 0:
        return [1]
    s = str(stone)
    if len(s) % 2 == 0:
        return [int(s[:len(s)//2]), int(s[len(s)//2:])]
    return [stone * 2024]

def apply(stones):
    for blink in range(25):
        stones = [num
                  for stone in stones
                  for num in transform(stone)]
        
    return len(stones)

def apply_smart(stones):
    from collections import Counter
    numbers = Counter(stones)
    
    for blink in range(75):
        new_numbers = Counter()
        for n, count in numbers.items():
            for stone in transform(n):
                new_numbers[stone] += count
        numbers = new_numbers
    
    return sum(numbers.values())

def solve_part1(stones):
    """Solve part 1 of the puzzle."""
    return apply(stones)

def solve_part2(stones):
    """Solve part 2 of the puzzle."""
    return apply_smart(stones)

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
