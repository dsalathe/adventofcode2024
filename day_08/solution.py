"""
Advent of Code 2024 - Day 8
https://adventofcode.com/2024/day/8
"""

from collections import defaultdict
from itertools import combinations

def parse_input(input_data):
    lines = [line.strip() for line in input_data.split('\n') if line.strip()]
    height = len(lines)
    width = len(lines[0])
    
    # Store antennas by frequency
    antennas = defaultdict(list)
    for y in range(height):
        for x in range(width):
            if lines[y][x] not in '.':
                freq = lines[y][x]
                antennas[freq].append((x, y))
    
    is_inbound = lambda x, y: 0 <= x < width and 0 <= y < height
    
    return is_inbound, antennas

def calculate_antinodes_part1(is_inbound, antenna_positions):
    antinodes = set()

    for (xm, ym), (xn, yn) in combinations(antenna_positions, 2):
        dx = xn - xm
        dy = yn - ym

        xl = xm - dx
        yl = ym - dy

        if is_inbound(xl, yl):
            antinodes.add((xl, yl))

        xo = xn + dx
        yo = yn + dy

        if is_inbound(xo, yo):
            antinodes.add((xo, yo))
    
    return antinodes

def calculate_antinodes_part2(is_inbound, antenna_positions):
    antinodes = set()
    for (xm, ym), (xn, yn) in combinations(antenna_positions, 2):
        dx = xn - xm
        dy = yn - ym

        x, y = xn, yn
        while is_inbound(x, y):
            antinodes.add((x, y))
            x += dx
            y += dy
        
        x, y = xm, ym
        while is_inbound(x, y):
            antinodes.add((x, y))
            x -= dx
            y -= dy

    return antinodes

def solve_part1(data):
    is_inbound, antennas = data
    all_antinodes = set()
    
    for freq, positions in antennas.items():
        all_antinodes |= calculate_antinodes_part1(is_inbound, positions)
    
    return len(all_antinodes)

def solve_part2(data):
    is_inbound, antennas = data
    all_antinodes = set()
    
    for freq, positions in antennas.items():
        all_antinodes |= calculate_antinodes_part2(is_inbound, positions)
    
    return len(all_antinodes)

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
