"""
Advent of Code 2024 - Day 14
https://adventofcode.com/2024/day/14
"""

from collections import deque

WIDTH, HEIGHT = 101, 103

def parse_input(input_data):
    robots = []
    for line in input_data.splitlines():
        if not line.strip():
            continue
        pos, vel = line.split()
        px, py = map(int, pos[2:].split(','))
        vx, vy = map(int, vel[2:].split(','))
        robots.append(((px, py), (vx, vy)))
    return robots

def update_robot(pos, vel):
    x, y = pos
    vx, vy = vel
    new_x = (x + vx) % WIDTH
    new_y = (y + vy) % HEIGHT
    return (new_x, new_y), vel


def componnent_size(positions, start_pos, seen):
    DIRS = [(-1,0), (0,1), (1,0), (0,-1)]
    queue = deque([start_pos])
    component_size = 0

    while queue:
        c = queue.popleft()
        if c in seen:
            continue
        seen.add(c)
        component_size += 1

        for dx, dy in DIRS:
            new_pos = c[0] + dx, c[1] + dy
            if new_pos in positions and new_pos not in seen:
                queue.append(new_pos)
    return component_size

def has_main_component(positions, n_agents):
    seen = set()
    for pos in positions:
        if pos not in seen and componnent_size(positions, pos, seen) >= n_agents // 4:
            return True
    return False

def solve_part1(robots):
    """Solve part 1 of the puzzle."""
    t = 100
    robots = [((px + vx * t) % WIDTH, (py + vy * t) % HEIGHT) for (px, py), (vx, vy) in robots]
    
    q1 = q2 = q3 = q4 = 0
    mx, my = WIDTH // 2, HEIGHT // 2
    
    for x, y in robots:
        if x < mx and y < my:
            q1 += 1
        elif x > mx and y < my:
            q2 += 1
        elif x < mx and y > my:
            q3 += 1
        elif x > mx and y > my:
            q4 += 1
    
    return q1 * q2 * q3 * q4

def solve_part2(robots):
    """Solve part 2 of the puzzle."""    
    for second in range(1, 10**6):
        robots = [update_robot(pos, vel) for pos, vel in robots]
        positions = {pos for pos, _ in robots}
        if has_main_component(positions, len(robots)):
            return second

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
