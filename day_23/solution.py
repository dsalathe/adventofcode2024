"""
Advent of Code 2024 - Day 23
https://adventofcode.com/2024/day/23
"""
from collections import defaultdict

def parse_input(input_data):
    """Parse the puzzle input into a graph representation."""
    graph = defaultdict(set)
    for line in input_data.splitlines():
        node1, node2 = line.strip().split('-')
        graph[node1].add(node2)
        graph[node2].add(node1)
    
    return graph

def find_triangles(graph):
    return {tuple(sorted((node1, node2, node3)))
            for node1 in graph for node2 in graph[node1] for node3 in graph[node2]
            if node3 in graph[node1] and node3 != node1}

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    graph = parse_input(data)
    triangles = find_triangles(graph)
    return sum(any(node.startswith('t') for node in triangle) for triangle in triangles)

def find_max_clique(graph):
    def bron_kerbosch(r, p):
        """Simplified and functional style of https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm"""
        subsets = lambda p: [(p[i], set(p[:i])) for i in range(len(p))]  
        return max([bron_kerbosch(r | {v}, p & graph[v]) for v, p in subsets(list(p))], key=len, default=r)
    
    return bron_kerbosch(set(), list(graph.keys()))

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    graph = parse_input(data)
    max_clique = find_max_clique(graph)    
    return ','.join(sorted(max_clique))

def main(input_file="input/input.txt"):
    """Main function to run the solution."""
    # Read input
    with open(input_file) as f:
        input_data = f.read()
    
    # Solve parts
    part1_solution = solve_part1(input_data)
    print(f"Part 1: {part1_solution}")
    
    part2_solution = solve_part2(input_data)
    print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()