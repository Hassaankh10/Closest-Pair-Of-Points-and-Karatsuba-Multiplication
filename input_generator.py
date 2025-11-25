"""
Input Generator for Divide and Conquer Algorithms
Generates random input files for:
1. Closest Pair of Points
2. Integer Multiplication
"""

import random
import os


def generate_closest_pair_input(filename, num_points, min_coord=-1000, max_coord=1000):
    """
    Generate random points for closest pair problem
    Format: Each line contains x y coordinates
    """
    points = []
    for _ in range(num_points):
        x = random.uniform(min_coord, max_coord)
        y = random.uniform(min_coord, max_coord)
        points.append((x, y))
    
    with open(filename, 'w') as f:
        f.write(f"{num_points}\n")
        for x, y in points:
            f.write(f"{x:.2f} {y:.2f}\n")
    
    return points


def generate_integer_multiplication_input(filename, num_digits1, num_digits2):
    """
    Generate random integers for multiplication problem
    Format: Two integers on separate lines
    """
    # Generate random integers with specified number of digits
    num1 = random.randint(10**(num_digits1-1), 10**num_digits1 - 1)
    num2 = random.randint(10**(num_digits2-1), 10**num_digits2 - 1)
    
    with open(filename, 'w') as f:
        f.write(f"{num1}\n")
        f.write(f"{num2}\n")
    
    return num1, num2


def generate_all_inputs():
    """Generate 10 input files for each algorithm"""
    
    # Create input directories
    os.makedirs("inputs/closest_pair", exist_ok=True)
    os.makedirs("inputs/integer_multiplication", exist_ok=True)
    
    # Generate 10 closest pair inputs with varying sizes (> 100 points)
    closest_pair_sizes = [150, 200, 250, 300, 350, 400, 500, 600, 750, 1000]
    
    print("Generating closest pair inputs...")
    for i, size in enumerate(closest_pair_sizes, 1):
        filename = f"inputs/closest_pair/input_{i:02d}_{size}points.txt"
        points = generate_closest_pair_input(filename, size)
        print(f"Generated {filename} with {len(points)} points")
    
    # Generate 10 integer multiplication inputs with varying digit sizes (> 100 digits)
    # We'll use number of digits as the "size" parameter
    multiplication_sizes = [
        (120, 120), (150, 150), (180, 180), (200, 200), (250, 250),
        (300, 300), (350, 350), (400, 400), (450, 450), (500, 500)
    ]
    
    print("\nGenerating integer multiplication inputs...")
    for i, (digits1, digits2) in enumerate(multiplication_sizes, 1):
        filename = f"inputs/integer_multiplication/input_{i:02d}_{digits1}x{digits2}digits.txt"
        num1, num2 = generate_integer_multiplication_input(filename, digits1, digits2)
        print(f"Generated {filename} with {digits1} and {digits2} digit numbers")


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    generate_all_inputs()
    print("\nAll input files generated successfully!")

