"""
Command-line demo to run algorithms on input files
"""

import os
import time
from algorithms import (
    Point,
    closest_pair_divide_conquer,
    karatsuba_multiply,
    standard_multiply
)


def run_closest_pair_demo():
    """Run closest pair algorithm on sample files"""
    print("=" * 70)
    print("CLOSEST PAIR OF POINTS - DEMONSTRATION")
    print("=" * 70)
    
    closest_dir = "inputs/closest_pair"
    if not os.path.exists(closest_dir):
        print(f"Error: {closest_dir} directory not found!")
        return
    
    # Test on a few sample files
    test_files = [
        "input_01_150points.txt",
        "input_05_350points.txt",
        "input_10_1000points.txt"
    ]
    
    for filename in test_files:
        filepath = os.path.join(closest_dir, filename)
        if not os.path.exists(filepath):
            continue
        
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        # Load points
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        num_points = int(lines[0].strip())
        points = []
        for i in range(1, num_points + 1):
            x, y = map(float, lines[i].strip().split())
            points.append(Point(x, y))
        
        print(f"Loaded {num_points} points")
        
        # Run algorithm
        start_time = time.time()
        distance, pair = closest_pair_divide_conquer(points)
        execution_time = (time.time() - start_time) * 1000
        
        print(f"\nResults:")
        print(f"  Closest Distance: {distance:.6f}")
        print(f"  Point 1: ({pair[0].x:.2f}, {pair[0].y:.2f})")
        print(f"  Point 2: ({pair[1].x:.2f}, {pair[1].y:.2f})")
        print(f"  Execution Time: {execution_time:.4f} ms")
        print(f"  Time per Point: {execution_time/num_points:.6f} ms")


def run_integer_mult_demo():
    """Run integer multiplication algorithm on sample files"""
    print("\n\n" + "=" * 70)
    print("INTEGER MULTIPLICATION (KARATSUBA) - DEMONSTRATION")
    print("=" * 70)
    
    int_dir = "inputs/integer_multiplication"
    if not os.path.exists(int_dir):
        print(f"Error: {int_dir} directory not found!")
        return
    
    # Test on a few sample files
    test_files = [
        "input_01_120x120digits.txt",
        "input_05_250x250digits.txt",
        "input_10_500x500digits.txt"
    ]
    
    for filename in test_files:
        filepath = os.path.join(int_dir, filename)
        if not os.path.exists(filepath):
            continue
        
        print(f"\n{'='*70}")
        print(f"Processing: {filename}")
        print(f"{'='*70}")
        
        # Load numbers
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        num1 = int(lines[0].strip())
        num2 = int(lines[1].strip())
        
        digits1 = len(str(num1))
        digits2 = len(str(num2))
        
        print(f"Number 1: {digits1} digits")
        print(f"Number 2: {digits2} digits")
        print(f"Number 1 (first 50 digits): {str(num1)[:50]}...")
        print(f"Number 2 (first 50 digits): {str(num2)[:50]}...")
        
        # Run Karatsuba
        start_karatsuba = time.time()
        karatsuba_result = karatsuba_multiply(num1, num2)
        karatsuba_time = (time.time() - start_karatsuba) * 1000
        
        # Run standard (for verification)
        start_standard = time.time()
        standard_result = standard_multiply(num1, num2)
        standard_time = (time.time() - start_standard) * 1000
        
        # Verify correctness
        is_correct = (karatsuba_result == standard_result)
        
        print(f"\nResults:")
        print(f"  Karatsuba Time: {karatsuba_time:.4f} ms")
        print(f"  Standard Time: {standard_time:.4f} ms")
        if standard_time > 0:
            speedup = standard_time / karatsuba_time if karatsuba_time > 0 else 0
            print(f"  Speedup: {speedup:.2f}x")
        print(f"  Correctness: {'✓ CORRECT' if is_correct else '✗ INCORRECT'}")
        print(f"  Result (first 100 digits): {str(karatsuba_result)[:100]}...")
        print(f"  Result (last 20 digits): ...{str(karatsuba_result)[-20:]}")


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("DIVIDE AND CONQUER ALGORITHMS - DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo runs both algorithms on sample input files.")
    print("For full GUI interface, run: python3 gui.py\n")
    
    try:
        run_closest_pair_demo()
        run_integer_mult_demo()
        
        print("\n\n" + "=" * 70)
        print("DEMONSTRATION COMPLETE")
        print("=" * 70)
        print("\nTo use the full GUI interface:")
        print("  python3 gui.py")
        print("\nTo test all algorithms:")
        print("  python3 test_algorithms.py")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

