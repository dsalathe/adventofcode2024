"""
Advent of Code 2024 - Day 15
https://adventofcode.com/2024/day/15
"""

from dataclasses import dataclass

@dataclass
class Box:
    x: int
    y: int
    width: int = 1

    @property
    def position(self): # Immutable. Useful for Sets
        return self.x, self.y

def parse_input(input_data):
    """Parse the puzzle input."""
    warehouse, instructions = input_data.strip().split('\n\n')
    return [list(line) for line in warehouse.splitlines()], instructions.replace('\n', '')

def scale_warehouse(warehouse):
    return [[c2 
             for c in row 
             for c2 in 
            {'#': ['#', '#'],
             'O': ['[', ']'],
             '.': ['.', '.'],
             '@': ['@', '.']
             }[c]]
            for row in warehouse]

def parse_warehouse(warehouse):
    player, boxes, walls = None, [], set()

    for y, row in enumerate(warehouse):
        for x, c in enumerate(row):
            if c == '@':
                player = Box(x, y)
            elif c == 'O':
                boxes.append(Box(x, y))
            elif c == '#':
                walls.add((x, y))
            elif c == '[':
                boxes.append(Box(x, y, 2))

    return player, boxes, walls

def collides(box1: Box, box2: Box):
    return (box1.x < box2.x + box2.width and
            box1.x + box1.width > box2.x and
            box1.y == box2.y)

def simulate_push(pusher: Box, boxes, walls, dx, dy, pushed=None):
    pushed = pushed or set()
    if any((pusher.x + i, pusher.y) in walls for i in range(pusher.width)):
        return False, []
    
    moves = []
    for box in boxes:
        if box.position not in pushed and collides(pusher, box):
            pushed.add(box.position)
            new_pusher = Box(box.x + dx, box.y + dy, box.width)
            is_valid, moved = simulate_push(new_pusher, boxes, walls, dx, dy, pushed)
            if not is_valid:
                return False, []
            moves.append((box, dx, dy))
            moves.extend(moved)
    return True, moves

DIRS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}

def run_instructions(warehouse, instructions):
    player, boxes, walls = parse_warehouse(warehouse)
    
    for instr in instructions:
        dx, dy = DIRS[instr]
        new_pos = Box(player.x + dx, player.y + dy)
        valid, moves = simulate_push(new_pos, boxes, walls, dx, dy)
        if valid:
            player = new_pos
            for box, dx, dy in moves:
                box.x += dx
                box.y += dy
    return sum(100 * box.y + box.x for box in boxes)


def solve_part1(data):
    """Solve part 1 of the puzzle."""
    warehouse, instructions = data
    return run_instructions(warehouse, instructions)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    warehouse, instructions = data
    return run_instructions(scale_warehouse(warehouse), instructions)

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