"""
Advent of Code 2024 - Day 22
https://adventofcode.com/2024/day/22
"""
from collections import defaultdict

MOD = 16777216

def parse_input(input_data):
    return [int(line.strip()) for line in input_data.split('\n') if line.strip()]

def generate_next_secret(secret):
    secret ^= (secret * 64)
    secret %= MOD
    secret ^= (secret // 32)
    secret %= MOD
    secret ^= (secret * 2048)
    secret %= MOD
    return secret

def generate_nth_secret(initial_secret, n):
    secret = initial_secret
    for _ in range(n):
        secret = generate_next_secret(secret)
    return secret

def get_price_arrays(buyers):
    all_prices = []
    for initial_secret in buyers:
        secrets = [initial_secret]
        s = initial_secret
        for _ in range(2000):
            s = generate_next_secret(s)
            secrets.append(s)

        prices = [x % 10 for x in secrets]
        all_prices.append(prices)
    return all_prices

def solve_part1(data):
    """Solve part 1 of the puzzle."""
    return sum(generate_nth_secret(initial, 2000) for initial in data)

def solve_part2(data):
    """Solve part 2 of the puzzle."""
    all_prices = get_price_arrays(data)
    pattern_dict = defaultdict(lambda: [0] * len(data))
    
    for buyer, prices in enumerate(all_prices):
        changes = [p2 - p1 for p1, p2 in zip(prices, prices[1:])]

        for c1, c2, c3, c4, price in zip(changes, changes[1:], changes[2:], changes[3:], prices[4:]):
            pattern = (c1, c2, c3, c4)
            if pattern_dict[pattern][buyer] == 0:
                pattern_dict[pattern][buyer] = price
                
    return max([sum(buyer_sells) for buyer_sells in pattern_dict.values()])

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