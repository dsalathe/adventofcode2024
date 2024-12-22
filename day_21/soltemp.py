"""
Advent of Code 2024 - Day 22
https://adventofcode.com/2024/day/22

Important observations:
1. we need to move as less as possible. So doing >>^^ would always be better
   than interleaving the moves like >^>^, because pressing the same key twice avoids moving.
   => This means we should only test full horizontal then vertical mvoes or vice versa.
2. Solving one layer at a time is not enough, because the output shortest path of some layer
   might not be the optimal input for the next layer.
3. Solving one character at a time across each layer is the key and works fine, because
   every layer needs to be reset to 'A' (for pushing the button) making each character computation independent.
4. Because each code ends with 'A' we can simplify a bit how to handle each layer.
"""

from functools import cache

def parse_input(input_data):
    """Parse the puzzle input."""
    return [line.strip() for line in input_data.split('\n') if line.strip()]

class DoorCodeSolver:
    def __init__(self, total_layers):
        self.number_pad = {
            char: (x, y)
            for y, row in enumerate([
                ["7" , "8", "9"],
                ["4" , "5", "6"],
                ["1" , "2", "3"],
                [None, "0", "A"]
            ])
            for x, char in enumerate(row)
            if char is not None
        }

        self.dir_pad = {
            char: (x, y)
            for y, row in enumerate([
                [None, "^", "A"],
                ["<" , "v", ">"]
            ])
            for x, char in enumerate(row)
            if char is not None
        }
        
        self.final_layer = total_layers

    def is_numeric(self, layer):
        return layer == self.final_layer

    def get_layout(self, layer):
        return self.number_pad if self.is_numeric(layer) else self.dir_pad

    def get_position(self, layer, code):
        return self.get_layout(layer)[code]

    #TODO: might refactor without using a class: we could have a boolean is_numeric default to False and first call with True  
    @cache
    def shortest_path(self, start_symbol, end_symbol, layer=None):
        if layer is None:
            layer = self.final_layer
                
        start = self.get_position(layer, start_symbol)
        end = self.get_position(layer, end_symbol)

        if layer == 0:
            return 1

        dist_v = abs(end[1] - start[1])
        dist_h = abs(end[0] - start[0])
        v = "^" if end[1] < start[1] else "v" if end[1] > start[1] else None
        h = "<" if end[0] < start[0] else ">" if end[0] > start[0] else None

        if dist_v == dist_h == 0:
            return self.shortest_path("A", "A", layer - 1)
        if dist_v == 0:
            return (self.shortest_path("A", h, layer - 1) + 
                   (dist_h - 1) * self.shortest_path(h, h, layer - 1) + 
                   self.shortest_path(h, "A", layer - 1))
        if dist_h == 0:
            return (self.shortest_path("A", v, layer - 1) + 
                   (dist_v - 1) * self.shortest_path(v, v, layer - 1) + 
                   self.shortest_path(v, "A", layer - 1))

        horizontal_first = (
            self.shortest_path("A", h, layer - 1) + 
            (dist_h - 1) * self.shortest_path(h, h, layer - 1) +
            self.shortest_path(h, v, layer - 1) + 
            (dist_v - 1) * self.shortest_path(v, v, layer - 1) + 
            self.shortest_path(v, "A", layer - 1)
        )

        vertical_first = (
            self.shortest_path("A", v, layer - 1) + 
            (dist_v - 1) * self.shortest_path(v, v, layer - 1) +
            self.shortest_path(v, h, layer - 1) + 
            (dist_h - 1) * self.shortest_path(h, h, layer - 1) + 
            self.shortest_path(h, "A", layer - 1)
        )

        if self.is_numeric(layer):
            force_horizontal_first = start[0] == 0 and end[1] == 3
            force_vertical_first = end[0] == 0 and start[1] == 3
        else:
            force_horizontal_first = start[0] == 0
            force_vertical_first = end[0] == 0

        if force_horizontal_first:
            return horizontal_first
        
        if force_vertical_first:
            return vertical_first
            
        return min(horizontal_first, vertical_first)
    
def solve(data, total_layers):
    solver = DoorCodeSolver(total_layers)
    total_complexity = 0
    
    for code in data:
        numeric_value = int(code[:-1])
        total_steps = sum(solver.shortest_path(start_symbol, end_symbol) 
                          for start_symbol, end_symbol in zip("A" + code, code))
            
        complexity = numeric_value * total_steps
        total_complexity += complexity
        
    return total_complexity

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    return solve(data, 3)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    return solve(data, 26)

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
    if part2_solution is not None:
        print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()