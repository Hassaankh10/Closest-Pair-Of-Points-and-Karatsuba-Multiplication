"""
Divide and Conquer Algorithms Implementation
1. Closest Pair of Points
2. Integer Multiplication (Karatsuba)
"""

import math
import sys


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def distance(self, other):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


def closest_pair_brute_force(points):
    """Brute force approach for closest pair (used for small sets)"""
    min_dist = float('inf')
    pair = None
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = points[i].distance(points[j])
            if dist < min_dist:
                min_dist = dist
                pair = (points[i], points[j])
    return min_dist, pair


def closest_pair_divide_conquer(points):
    """
    Divide and conquer algorithm for finding closest pair of points
    Time Complexity: O(n log² n)
    """
    # Sort points by x-coordinate
    points_sorted_x = sorted(points, key=lambda p: p.x)
    
    def closest_pair_rec(px, py):
        n = len(px)
        
        # Base case: use brute force for small sets
        if n <= 3:
            return closest_pair_brute_force(px)
        
        # Divide: split points into left and right halves
        mid = n // 2
        mid_point = px[mid]
        
        pyl = [p for p in py if p.x <= mid_point.x]
        pyr = [p for p in py if p.x > mid_point.x]
        
        # Conquer: recursively find closest pairs in left and right
        dl, pair_l = closest_pair_rec(px[:mid], pyl)
        dr, pair_r = closest_pair_rec(px[mid:], pyr)
        
        # Find minimum of two halves
        d = min(dl, dr)
        min_pair = pair_l if dl < dr else pair_r
        
        # Combine: check points in the strip
        strip = [p for p in py if abs(p.x - mid_point.x) < d]
        
        # Check points in strip (at most 7 comparisons per point)
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j].y - strip[i].y) < d:
                dist = strip[i].distance(strip[j])
                if dist < d:
                    d = dist
                    min_pair = (strip[i], strip[j])
                j += 1
        
        return d, min_pair
    
    # Sort points by y-coordinate for strip checking
    points_sorted_y = sorted(points, key=lambda p: p.y)
    
    return closest_pair_rec(points_sorted_x, points_sorted_y)


def karatsuba_multiply(x, y):
    """
    Karatsuba algorithm for integer multiplication
    Time Complexity: O(n^log2(3)) ≈ O(n^1.585)
    """
    # Convert to strings to handle large integers
    x_str = str(x)
    y_str = str(y)
    
    # Base case: if numbers are small, use standard multiplication
    if len(x_str) == 1 or len(y_str) == 1:
        return x * y
    
    # Make both strings same length by padding with zeros
    n = max(len(x_str), len(y_str))
    if n % 2 != 0:
        n += 1
    
    x_str = x_str.zfill(n)
    y_str = y_str.zfill(n)
    
    # Split numbers into halves
    mid = n // 2
    
    a = int(x_str[:mid])
    b = int(x_str[mid:])
    c = int(y_str[:mid])
    d = int(y_str[mid:])
    
    # Recursive calls
    ac = karatsuba_multiply(a, c)
    bd = karatsuba_multiply(b, d)
    ad_bc = karatsuba_multiply(a + b, c + d) - ac - bd
    
    # Combine results: 10^n * ac + 10^(n/2) * (ad + bc) + bd
    result = (10 ** n) * ac + (10 ** mid) * ad_bc + bd
    
    return result


def standard_multiply(x, y):
    """Standard multiplication for comparison"""
    return x * y


if __name__ == "__main__":
    # Test closest pair
    points = [Point(2, 3), Point(12, 30), Point(40, 50), Point(5, 1), Point(12, 10), Point(3, 4)]
    dist, pair = closest_pair_divide_conquer(points)
    print(f"Closest pair: {pair[0]} and {pair[1]}, Distance: {dist:.2f}")
    
    # Test Karatsuba
    x = 1234
    y = 5678
    result = karatsuba_multiply(x, y)
    print(f"Karatsuba: {x} * {y} = {result}")
    print(f"Standard: {x} * {y} = {x * y}")

