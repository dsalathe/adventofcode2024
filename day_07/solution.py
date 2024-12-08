"""
Advent of Code 2024 - Day 7
https://adventofcode.com/2024/day/7
"""

from itertools import product
from operator import add, mul

def parse_input(input_data):
    equations = []
    for line in input_data.split('\n'):
        if not line.strip():
            continue
        
        test_value, numbers = line.split(':')
        test_value = int(test_value)
        numbers = [int(x) for x in numbers.strip().split()]
        equations.append((test_value, numbers))
    return equations

def evaluate_expression(numbers, operators):
    result = numbers[0]
    for operator, number in zip(operators, numbers[1:]):
        result = operator(result, number)
    return result

def can_make_test_value(test_value, numbers, operators):
    return any(
        evaluate_expression(numbers, ops) == test_value 
        for ops in product(operators, repeat=len(numbers) - 1))
    

def solve_part1(data):
    return sum(test_value 
               for test_value, numbers in data 
               if can_make_test_value(test_value, numbers, [add, mul]))

def solve_part2(data):
    concat = lambda x, y: int(str(x) + str(y))
    return sum(test_value 
               for test_value, numbers in data 
               if can_make_test_value(test_value, numbers, [add, mul, concat]))

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
