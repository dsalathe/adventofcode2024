"""
Advent of Code 2024 - Day 20
https://adventofcode.com/2024/day/20
"""

from collections import deque
from itertools import product

def parse_input(input_data):
    """Parse the puzzle input into a 2D grid."""
    grid = [list(line.strip()) for line in input_data.split('\n') if line.strip()]
    is_inside = lambda x, y: 0 <= x < len(grid[0]) and 0 <= y < len(grid)
    return is_inside, grid

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find_positions(grid, chars):
    positions = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in chars:
                positions[cell] = (x, y)
    return positions

def bfs(grid, is_inside, start):
    distances = [[float('inf') for _ in row] for row in grid]
    distances[start[1]][start[0]] = 0
    
    queue = deque([start])
    
    while queue:
        x, y = queue.popleft()
        current_dist = distances[y][x]
        
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if is_inside(new_x, new_y) and grid[new_y][new_x] != '#' and distances[new_y][new_x] > current_dist + 1:
                distances[new_y][new_x] = current_dist + 1
                queue.append((new_x, new_y))
                
    return distances

def compute_distances(grid, is_inside):
    positions = find_positions(grid, 'SE')
    start, end = positions['S'], positions['E']
    
    dist_from_start = bfs(grid, is_inside, start)
    dist_from_end = bfs(grid, is_inside, end)
    normal_dist = dist_from_start[end[1]][end[0]]
    
    return dist_from_start, dist_from_end, normal_dist

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def reachable_from(grid, distances):
    return {(x, y, distances[y][x])
            for y, row in enumerate(grid)
            for x, e in enumerate(row)
            if e != '#' and distances[y][x] != float('inf')}

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    is_inside, grid = data
    dist_from_start, dist_from_end, normal_dist = compute_distances(grid, is_inside)
    shortcuts = set()

    for x, y, dist_start in reachable_from(grid, dist_from_start):
        for (dx1, dy1), (dx2, dy2) in product(DIRECTIONS, repeat=2):
            fx, fy = x + dx1 + dx2, y + dy1 + dy2
            if is_inside(fx, fy) and grid[fy][fx] != '#' and dist_from_end[fy][fx] != float('inf'):
                # It is okay to abuse with "+2" because if we went back we would have use the same path
                route_with_shortcut = dist_start + 2 + dist_from_end[fy][fx]
                if normal_dist - route_with_shortcut >= 100:
                    shortcuts.add((x, y, fx, fy))
    return len(shortcuts)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    is_inside, grid = data
    dist_from_start, dist_from_end, normal_dist = compute_distances(grid, is_inside)
    shortcuts = set()

    for x, y, dist_start in reachable_from(grid, dist_from_start):
        for fx, fy, dist_end in reachable_from(grid, dist_from_end):
            if (dist := manhattan_distance(x, y, fx, fy)) <= 20:
                route_with_shortcut = dist_start + dist + dist_end
                if normal_dist - route_with_shortcut >= 100:
                    shortcuts.add((x, y, fx, fy))
    return len(shortcuts)

def main(input_file: str = "input/input.txt"):
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