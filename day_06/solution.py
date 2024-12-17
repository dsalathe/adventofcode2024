"""
Advent of Code 2024 - Day 6
https://adventofcode.com/2024/day/6
"""

def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]

def find_start(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '^':
                return i, j
    return -1, -1


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)] # Clockwise order, facing up first

def move(x, y, dir):
    dx, dy = DIRECTIONS[dir]
    return x + dx, y + dy

def is_inside(row, col, grid):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def count_path_steps(grid):        
    current_row, current_col, current_dir = *find_start(grid), 0 # Start facing up
    visited = set()

    while is_inside(current_row, current_col, grid):
        visited.add((current_row, current_col))
        new_row, new_col = move(current_row, current_col, current_dir)
            
        if grid[new_row][new_col] == '#':
            current_dir = (current_dir + 1) % 4 # Turn right
        else:
            current_row, current_col = new_row, new_col
    return len(visited)


def has_loop(grid, added_obstacle):    
    visited_states = set() # Now we need direction too. State is defined as: row, col, dir
    current_row, current_col, current_dir = *find_start(grid), 0 # Start facing up
    
    while (current_state := (current_row, current_col, current_dir)) not in visited_states:
        visited_states.add(current_state)
        new_row, new_col = move(*current_state)
        
        if not is_inside(new_row, new_col, grid):
            return False
                    
        if grid[new_row][new_col] == '#' or (new_row, new_col) == added_obstacle:
            current_dir = (current_dir + 1) % 4
        else:
            current_row, current_col = new_row, new_col           
    return True
        

def simulate_all_obstacles(grid):
    return sum(
            cell in {'.', '^'} and has_loop(grid, (i, j))
            for i, row in enumerate(grid) 
            for j, cell in enumerate(row)
        )

def solve_part1(grid):
    """Solve part 1 of the puzzle."""
    return count_path_steps(grid)

def solve_part2(grid):
    """Solve part 2 of the puzzle."""
    return simulate_all_obstacles(grid)

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
