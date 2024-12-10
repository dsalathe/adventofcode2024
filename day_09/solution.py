"""
Advent of Code 2024 - Day 9
https://adventofcode.com/2024/day/9
"""

from dataclasses import dataclass

def parse_input(input_data):
    return input_data.strip()

def expand_disk_map(disk_map):
    expanded = []
    for i, length in enumerate(map(int, disk_map)):
        expanded.extend(([i//2] if i % 2 == 0 else ['.']) * length)
    return expanded

def compact_files(disk_map):
    disk = expand_disk_map(disk_map).copy()

    find_next_space = lambda start: next((i for i in range(start, len(disk)) if disk[i] == '.'))
    find_next_file = lambda start: next((i for i in range(start, -1, -1) if disk[i] != '.'))

    space_ptr = find_next_space(0)  
    file_ptr = find_next_file(len(disk) - 1) 
    
    while space_ptr < file_ptr:
        disk[space_ptr], disk[file_ptr] = disk[file_ptr], disk[space_ptr]
        
        space_ptr = find_next_space(space_ptr + 1)
        file_ptr = find_next_file(file_ptr - 1)
    
    return disk

@dataclass
class FileInfo:
    id: int
    start: int
    size: int

def build_file_index(disk):
    files = []
    for i, block in enumerate(disk):
        if block != '.':
            if block >= len(files):
                files.append(FileInfo(block, i, 1))
            else:
                files[block].size += 1
    return files

def find_best_position(disk, file_start, file_size):
    current_free = 0
    for i in range(file_start):
        if disk[i] == '.':
            current_free += 1
            if current_free == file_size:
                return i - file_size + 1
        else:
            current_free = 0
    return -1

def compact_whole_files(disk_map):
    disk = expand_disk_map(disk_map).copy()    
    files = build_file_index(disk)
    
    for file_info in reversed(files):
        file_id = file_info.id
        file_size = file_info.size
        file_start = file_info.start
        best_position = find_best_position(disk, file_start, file_size)
        
        if best_position != -1:
            for i in range(file_start, file_start + file_size):
                disk[i] = '.'
                
            for i in range(best_position, best_position + file_size):
                disk[i] = file_id
    
    return disk

def calculate_checksum(compacted):
    return sum(pos * block for pos, block in enumerate(compacted) if block != '.')

def solve_part1(disk_map):
    """Solve part 1 of the puzzle."""
    compacted = compact_files(disk_map)
    return calculate_checksum(compacted)

def solve_part2(disk_map):
    """Solve part 2 of the puzzle."""
    compacted = compact_whole_files(disk_map)
    return calculate_checksum(compacted)

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
