"""
Advent of Code 2024 - Day 18
https://adventofcode.com/2024/day/18
"""

from simpledsa import PriorityQueue

SIDE = 71

def parse_input(input_data):
    """Parse the puzzle input."""
    return [tuple(map(int, line.strip().split(','))) for line in input_data.split('\n') if line.strip()]

def get_grid():
    return [['.' for _ in range(SIDE)] for _ in range(SIDE)]

def place_bits(grid, bits):
    for x, y in bits:
        grid[y][x] = '#'
    return grid

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_neighbors(pos, grid):
    x, y = pos
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < SIDE and 0 <= new_y < SIDE and grid[new_y][new_x] != '#':
            neighbors.append((new_x, new_y))
    return neighbors

def shortest_path(grid, start, end):
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}
    queue = PriorityQueue()
    queue.push(start, priority=f_score[start])
    visited = set()

    while queue:
        current = queue.pop()
        
        if current == end:
            return g_score[current]
        
        if current in visited:
            continue
            
        visited.add(current)
        
        for next_pos in get_neighbors(current, grid):
            if next_pos not in visited:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(next_pos, float('inf')):
                    g_score[next_pos] = tentative_g
                    f_score[next_pos] = tentative_g + manhattan_distance(next_pos, end)
                    queue.push(next_pos, priority=f_score[next_pos])
    
    return -1

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    grid = place_bits(get_grid(), data[:1024])
    start = (0, 0)
    end = (70, 70) 
    return shortest_path(grid, start, end)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    grid = get_grid()
    start = (0, 0)
    end = (70, 70)
    shortest = float("inf")

    for x,y in data:
        grid[y][x] = '#'
        result = shortest_path(grid, start, end)
        if result != -1:
            shortest = min(shortest, result)
        else:
            return f"{x},{y}"

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