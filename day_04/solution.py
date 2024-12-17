"""
Advent of Code 2024 - Day 4
https://adventofcode.com/2024/day/4
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]

def find_word(grid, word, directions, output_transform, result):
    rows = len(grid)
    cols = len(grid[0])
    
    def check_direction(row, col, dx, dy):
        depth = len(word) - 1
        if not (0 <= row + depth*dx < rows and 0 <= col + depth*dy < cols):
            return False
        
        return all(grid[row + i*dx][col + i*dy] == word[i] for i in range(len(word)))
    
    for row in range(rows):
        for col in range(cols):
            for dx, dy in directions:
                if check_direction(row, col, dx, dy):
                    result = output_transform(result, row, col, dx, dy)

    return result


ALL_DIRECTIONS      = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 or  y != 0]
DIAGONAL_DIRECTIONS = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if x != 0 and y != 0]


def solve_part1(data):
    """Solve part 1 of the puzzle."""
    return find_word(data, "XMAS", ALL_DIRECTIONS, lambda result, *_: result + 1, 0)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    center_positions = find_word(data, "MAS", DIAGONAL_DIRECTIONS,
                                 lambda result, x, y, dx, dy: result + [(x+dx, y+dy)], [])
    
    from collections import Counter
    return sum(1 for count in Counter(center_positions).values() if count == 2)

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
