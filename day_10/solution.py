"""
Advent of Code 2024 - Day 10
https://adventofcode.com/2024/day/10
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    grid = [list(map(int, line.strip())) for line in input_data.split('\n') if line.strip()]
    is_inside = lambda x, y: 0 <= x < len(grid[0]) and 0 <= y < len(grid)
    return is_inside, grid

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def find_peaks(is_inside, grid, x, y, peaks):
    if grid[y][x] == 9:
        peaks.add((x, y))
        return peaks
    for d in DIRECTIONS:
        new_x, new_y = x + d[0], y + d[1]
        if is_inside(new_x, new_y) and grid[new_y][new_x] - 1 == grid[y][x]:
            find_peaks(is_inside, grid, new_x, new_y, peaks)
    return peaks

def count_trails(is_inside, grid, x, y, total):
    if grid[y][x] == 9:
        return total + 1
    for d in DIRECTIONS:
        new_x, new_y = x + d[0], y + d[1]
        if is_inside(new_x, new_y) and grid[new_y][new_x] - 1 == grid[y][x]:
            total = count_trails(is_inside, grid, new_x, new_y, total)
    return total


def solve_part1(data):
    """Solve part 1 of the puzzle."""
    is_inside, grid = data
    total = 0
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 0:
                total += len(find_peaks(is_inside, grid, x, y, set()))
    return total

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    is_inside, grid = data
    total = 0
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 0:
                total += count_trails(is_inside, grid, x, y, 0)
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
