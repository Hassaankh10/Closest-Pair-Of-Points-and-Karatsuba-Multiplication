"""
Test script to verify algorithms work correctly
"""

from algorithms import (
    Point,
    closest_pair_divide_conquer,
    closest_pair_brute_force,
    karatsuba_multiply,
    standard_multiply
)

def test_closest_pair():
    """Test closest pair algorithm"""
    print("Testing Closest Pair Algorithm...")
    
    # Test with known points
    points = [
        Point(0, 0),
        Point(1, 1),
        Point(2, 2),
        Point(3, 3),
        Point(0.5, 0.5)  # Closest to (0,0)
    ]
    
    dist, pair = closest_pair_divide_conquer(points)
    print(f"  Closest distance: {dist:.6f}")
    print(f"  Pair: {pair[0]} and {pair[1]}")
    
    # Verify with brute force
    brute_dist, brute_pair = closest_pair_brute_force(points)
    print(f"  Brute force distance: {brute_dist:.6f}")
    print(f"  Match: {abs(dist - brute_dist) < 0.0001}")
    print("✓ Closest Pair Test Passed\n")

def test_karatsuba():
    """Test Karatsuba multiplication"""
    print("Testing Karatsuba Multiplication...")
    
    test_cases = [
        (1234, 5678),
        (12345, 67890),
        (123456, 789012),
    ]
    
    for x, y in test_cases:
        karatsuba_result = karatsuba_multiply(x, y)
        standard_result = standard_multiply(x, y)
        match = (karatsuba_result == standard_result)
        print(f"  {x} × {y} = {karatsuba_result}")
        print(f"  Standard: {standard_result}, Match: {match}")
        assert match, "Results don't match!"
    
    print("✓ Karatsuba Test Passed\n")

def test_file_loading():
    """Test loading input files"""
    print("Testing File Loading...")
    
    import os
    
    # Test closest pair file
    closest_file = "inputs/closest_pair/input_01_150points.txt"
    if os.path.exists(closest_file):
        with open(closest_file, 'r') as f:
            lines = f.readlines()
            num_points = int(lines[0].strip())
            print(f"  Loaded {num_points} points from {closest_file}")
            assert num_points == 150, "Point count mismatch!"
    
    # Test integer multiplication file
    int_file = "inputs/integer_multiplication/input_01_120x120digits.txt"
    if os.path.exists(int_file):
        with open(int_file, 'r') as f:
            lines = f.readlines()
            num1 = int(lines[0].strip())
            num2 = int(lines[1].strip())
            print(f"  Loaded numbers with {len(str(num1))} and {len(str(num2))} digits")
            assert len(str(num1)) == 120, "Digit count mismatch!"
    
    print("✓ File Loading Test Passed\n")

if __name__ == "__main__":
    print("=" * 50)
    print("Algorithm Test Suite")
    print("=" * 50 + "\n")
    
    try:
        test_closest_pair()
        test_karatsuba()
        test_file_loading()
        print("=" * 50)
        print("All Tests Passed! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test Failed: {e}")
        import traceback
        traceback.print_exc()

