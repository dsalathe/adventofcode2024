"""
Advent of Code 2024 - Day 5
https://adventofcode.com/2024/day/5
"""
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class PuzzleData:
    dependencies: List[Tuple[int, int]]
    sequences: List[List[int]]


def parse_input(input_text: str) -> PuzzleData:
    """Parse input text into dependencies and sequences"""
    dependencies = []
    sequences = []
    
    lines = [line.strip() for line in input_text.split('\n') if line.strip()]
    
    for line in lines:
        if '|' in line:
            n1, n2 = map(int, line.split('|'))
            dependencies.append((n1, n2))
        else:
            numbers = [int(n) for n in line.split(',')]
            sequences.append(numbers)
    
    return PuzzleData(dependencies=dependencies, sequences=sequences)


def is_valid_sequence(sequence: List[int], dependencies: List[Tuple[int, int]]) -> bool:
    positions = {n: idx for idx, n in enumerate(sequence)}
    
    return all(
        positions[before] < positions[after]
        for before, after in dependencies
        if before in positions and after in positions
    )


def topological_sort(sequence: List[int], dependencies: List[Tuple[int, int]]) -> List[int]:
    """
    Kahn's algorithm for topological sorting
    """
    # Build graph and calculate in-degrees
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    
    for before, after in dependencies:
        if before in sequence and after in sequence:
            graph[before].add(after)
            in_degree[after] += 1
    
    # Start with nodes that have no dependencies
    queue = [node for node in sequence if in_degree[node] == 0]
    result = []
    
    while queue:
        node = queue.pop(0)
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result

def sum_middles(seqs):
    return sum(seq[len(seq)//2] for seq in seqs)


def solve_part1(data: PuzzleData) -> int:
    """Find sum of middle numbers in valid sequences"""
    valid_sequences = [seq for seq in data.sequences if is_valid_sequence(seq, data.dependencies)]
    return sum_middles(valid_sequences)


def solve_part2(data: PuzzleData) -> int:
    """Fix invalid sequences and sum their middle numbers"""
    invalid_sequences = [seq for seq in data.sequences if not is_valid_sequence(seq, data.dependencies)]
    return sum_middles([topological_sort(seq, data.dependencies) for seq in invalid_sequences])


def main(input_file: str = "input/input.txt") -> None:
    """Main entry point"""
    try:
        with open(input_file) as f:
            input_data = f.read()
        
        puzzle_data = parse_input(input_data)
        print(f"Part 1: {solve_part1(puzzle_data)}")
        print(f"Part 2: {solve_part2(puzzle_data)}")
    
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()