"""
Advent of Code 2024 - Day 12
https://adventofcode.com/2024/day/12
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    grid = [line.strip() for line in input_data.split('\n') if line.strip()]
    height, width = len(grid), len(grid[0])
    is_inbound = lambda x, y: 0 <= x < width and 0 <= y < height
    return is_inbound, grid

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find_region(grid, is_inbound, start_row, start_col, visited):
    if not is_inbound(start_row, start_col) or (start_row, start_col) in visited:
        return set()
    
    plant_type = grid[start_row][start_col]
    result = {(start_row, start_col)}
    visited.add((start_row, start_col))
    
    for dr, dc in DIRECTIONS:
        new_row, new_col = start_row + dr, start_col + dc
        if is_inbound(new_row, new_col) and grid[new_row][new_col] == plant_type:
            result |= find_region(grid, is_inbound, new_row, new_col, visited)
    
    return result

def get_perimeter_positions(is_inbound, region):
    perimeter_positions = set()
    for row, col in region:
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if not is_inbound(new_row, new_col) or (new_row, new_col) not in region:
                perimeter_positions.add((row, col, dr, dc))
    
    return perimeter_positions

def count_sides(perimeter_positions):
    from collections import defaultdict

    positions_by_orientation = defaultdict(list)
    for row, col, dr, dc in perimeter_positions:
        # Little hack to process vertical and horizontal edges in the same way
        positions_by_orientation[(dr, dc)].append((row, col) if dc == 0 else (col, row))
    
    for positions in positions_by_orientation.values():
        positions.sort()
    
    def count_continuous_edges(positions):
        count = 1
        prev_row, prev_col = positions[0]
        for row, col in positions[1:]:
            if row != prev_row or col != prev_col + 1:
                count += 1
            prev_row, prev_col = row, col
        return count
    
    return sum(
        count_continuous_edges(positions) 
        for positions in positions_by_orientation.values())

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    is_inbound, grid = data
    visited = set()
    total_price = 0
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) not in visited:
                region = find_region(grid, is_inbound, row, col, visited)
                area = len(region)
                perimeter = len(get_perimeter_positions(is_inbound, region))
                price = area * perimeter
                total_price += price
    
    return total_price

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    is_inbound, grid = data    
    visited = set()
    total_price = 0
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) not in visited:
                region = find_region(grid, is_inbound, row, col, visited)
                area = len(region)
                perimeter_positions = get_perimeter_positions(is_inbound, region)
                sides = count_sides(perimeter_positions)
                price = area * sides
                total_price += price
    
    return total_price

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
