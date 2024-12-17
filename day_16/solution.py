"""
Advent of Code 2024 - Day 15
https://adventofcode.com/2024/day/15
"""

from dataclasses import dataclass
from collections import defaultdict
from typing import Tuple
from simpledsa import PriorityQueue

EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)
NORTH = (-1, 0)

DIRECTION_TURNS = {
    NORTH: (EAST, WEST),
    EAST: (SOUTH, NORTH),
    SOUTH: (WEST, EAST),
    WEST: (NORTH, SOUTH),
}

def clockwise(dir):
    return DIRECTION_TURNS[dir][0]

def counterclockwise(dir):
    return DIRECTION_TURNS[dir][1]

@dataclass(frozen=True)
class State:
    position: Tuple[int, int]
    direction: Tuple[int, int]
    
def parse_input(input_data):
    grid = [line.strip() for line in input_data.split('\n') if line.strip()]
    is_inside = lambda row, col: 0 <= row < len(grid) and 0 <= col < len(grid[0])
    return is_inside, grid

def get_next_states(state: State, grid, is_inside):
    new_row = state.position[0] + state.direction[0]
    new_col = state.position[1] + state.direction[1]
    
    if is_inside(new_row, new_col) and grid[new_row][new_col] != '#':
        yield State((new_row, new_col), state.direction), 1
    
    for new_direction in (clockwise(state.direction), 
                        counterclockwise(state.direction)):
        yield State(state.position, new_direction), 1000

def find_positions(grid, chars):
    positions = {}
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell in chars:
                positions[cell] = (i, j)
    return positions

def find_optimal_paths(data):
    is_inside, grid = data
    positions = find_positions(grid, 'SE')
    start_state = State(positions['S'], EAST)
    end_pos = positions['E']
    
    distances = defaultdict(lambda: float('inf'))
    predecessors = defaultdict(set)
    distances[start_state] = 0
    min_end_cost = float('inf')
    end_states = set()
    
    with PriorityQueue() as queue:
        queue.push(start_state, priority=0)
        
        while queue:
            current_state = queue.pop()
            current_cost = distances[current_state]
            
            if current_state.position == end_pos:
                if current_cost < min_end_cost:
                    min_end_cost = current_cost
                    end_states = {current_state}
                elif current_cost == min_end_cost:
                    end_states.add(current_state)
                continue
            
            if current_cost > min_end_cost:
                continue
            
            for new_state, move_cost in get_next_states(current_state, grid, is_inside):
                new_cost = current_cost + move_cost
                
                if new_cost < distances[new_state]:
                    distances[new_state] = new_cost
                    predecessors[new_state].clear()
                    queue.push(new_state, priority=new_cost)
                if new_cost == distances[new_state]:
                    predecessors[new_state].add(current_state)
    
    def collect_path_tiles(state: State, visited):
        if state not in visited:
            visited.add(state)
            for pred in predecessors[state]:
                collect_path_tiles(pred, visited)
    
    visited = set()
    for end_state in end_states:
        collect_path_tiles(end_state, visited)
    
    return min_end_cost, {state.position for state in visited}

def solve_part1(data) -> int:
    return find_optimal_paths(data)[0]

def solve_part2(data) -> int:
    return len(find_optimal_paths(data)[1])

def main(input_file: str = "input/input.txt") -> None:
    with open(input_file) as f:
        data = parse_input(f.read())
    
    print(f"Part 1: {solve_part1(data)}")
    print(f"Part 2: {solve_part2(data)}")

if __name__ == "__main__":
    main()