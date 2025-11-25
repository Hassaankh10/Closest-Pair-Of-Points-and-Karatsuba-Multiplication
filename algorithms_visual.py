"""
Step-by-step visualization versions of divide and conquer algorithms
"""

import math
from algorithms import Point, closest_pair_brute_force


def closest_pair_divide_conquer_visual(points, step_callback=None, delay=0.5):
    """
    Divide and conquer algorithm with step-by-step visualization
    step_callback: function(step_type, data) called at each step
    """
    # Sort points by x-coordinate
    points_sorted_x = sorted(points, key=lambda p: p.x)
    
    if step_callback:
        step_callback('init', {
            'points': points,
            'num_points': len(points),
            'message': f'Initializing: {len(points)} points loaded'
        })
    
    def closest_pair_rec(px, py, level=0):
        n = len(px)
        indent = "  " * level
        
        if step_callback:
            step_callback('divide_start', {
                'points': px,
                'num_points': n,
                'level': level,
                'message': f'{indent}Processing {n} points (Level {level})'
            })
        
        # Base case: use brute force for small sets
        if n <= 3:
            if step_callback:
                step_callback('base_case', {
                    'points': px,
                    'message': f'{indent}Base case: {n} points, using brute force'
                })
            result = closest_pair_brute_force(px)
            if step_callback:
                step_callback('base_result', {
                    'points': px,
                    'distance': result[0],
                    'pair': result[1],
                    'message': f'{indent}Found closest pair: distance = {result[0]:.4f}'
                })
            return result
        
        # Divide: split points into left and right halves
        mid = n // 2
        mid_point = px[mid]
        
        if step_callback:
            step_callback('divide', {
                'all_points': px,
                'left_points': px[:mid],
                'right_points': px[mid:],
                'mid_point': mid_point,
                'mid_x': mid_point.x,
                'level': level,
                'message': f'{indent}Dividing at x = {mid_point.x:.2f} into {mid} and {n-mid} points'
            })
        
        pyl = [p for p in py if p.x <= mid_point.x]
        pyr = [p for p in py if p.x > mid_point.x]
        
        # Conquer: recursively find closest pairs in left and right
        if step_callback:
            step_callback('conquer_left', {
                'points': px[:mid],
                'level': level,
                'message': f'{indent}Recursively solving left half ({mid} points)'
            })
        
        dl, pair_l = closest_pair_rec(px[:mid], pyl, level + 1)
        
        if step_callback:
            step_callback('conquer_left_result', {
                'points': px[:mid],
                'distance': dl,
                'pair': pair_l,
                'level': level,
                'message': f'{indent}Left half result: distance = {dl:.4f}'
            })
        
        if step_callback:
            step_callback('conquer_right', {
                'points': px[mid:],
                'level': level,
                'message': f'{indent}Recursively solving right half ({n-mid} points)'
            })
        
        dr, pair_r = closest_pair_rec(px[mid:], pyr, level + 1)
        
        if step_callback:
            step_callback('conquer_right_result', {
                'points': px[mid:],
                'distance': dr,
                'pair': pair_r,
                'level': level,
                'message': f'{indent}Right half result: distance = {dr:.4f}'
            })
        
        # Find minimum of two halves
        d = min(dl, dr)
        min_pair = pair_l if dl < dr else pair_r
        
        if step_callback:
            step_callback('min_compare', {
                'left_distance': dl,
                'right_distance': dr,
                'min_distance': d,
                'min_pair': min_pair,
                'level': level,
                'message': f'{indent}Comparing: min({dl:.4f}, {dr:.4f}) = {d:.4f}'
            })
        
        # Combine: check points in the strip
        strip = [p for p in py if abs(p.x - mid_point.x) < d]
        
        if step_callback:
            step_callback('strip_identify', {
                'all_points': py,
                'strip_points': strip,
                'mid_point': mid_point,
                'strip_width': d,
                'level': level,
                'message': f'{indent}Checking strip: {len(strip)} points within distance {d:.4f}'
            })
        
        # Check points in strip (at most 7 comparisons per point)
        strip_improved = False
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j].y - strip[i].y) < d:
                dist = strip[i].distance(strip[j])
                if step_callback and j == i + 1:  # Show first comparison for each point
                    step_callback('strip_check', {
                        'strip_points': strip,
                        'checking': (strip[i], strip[j]),
                        'distance': dist,
                        'current_min': d,
                        'level': level,
                        'message': f'{indent}Checking pair in strip: distance = {dist:.4f}'
                    })
                if dist < d:
                    d = dist
                    min_pair = (strip[i], strip[j])
                    strip_improved = True
                    if step_callback:
                        step_callback('strip_update', {
                            'strip_points': strip,
                            'new_pair': min_pair,
                            'new_distance': d,
                            'level': level,
                            'message': f'{indent}Found closer pair in strip: distance = {d:.4f}'
                        })
                j += 1
        
        if step_callback:
            if strip_improved:
                step_callback('combine_result', {
                    'final_distance': d,
                    'final_pair': min_pair,
                    'level': level,
                    'message': f'{indent}Final result: distance = {d:.4f} (improved by strip)'
                })
            else:
                step_callback('combine_result', {
                    'final_distance': d,
                    'final_pair': min_pair,
                    'level': level,
                    'message': f'{indent}Final result: distance = {d:.4f} (from halves)'
                })
        
        return d, min_pair
    
    # Sort points by y-coordinate for strip checking
    points_sorted_y = sorted(points, key=lambda p: p.y)
    
    return closest_pair_rec(points_sorted_x, points_sorted_y)


def karatsuba_multiply_visual(x, y, step_callback=None, delay=0.3):
    """
    Karatsuba algorithm with step-by-step visualization
    step_callback: function(step_type, data) called at each step
    """
    x_str = str(x)
    y_str = str(y)
    
    if step_callback:
        step_callback('init', {
            'num1': x,
            'num2': y,
            'num1_str': x_str,
            'num2_str': y_str,
            'num1_digits': len(x_str),
            'num2_digits': len(y_str),
            'message': f'Initializing: {len(x_str)} × {len(y_str)} digits'
        })
    
    # Base case: if numbers are small, use standard multiplication
    if len(x_str) == 1 or len(y_str) == 1:
        if step_callback:
            step_callback('base_case', {
                'num1': x,
                'num2': y,
                'message': f'Base case: single digit, using standard multiplication'
            })
        result = x * y
        if step_callback:
            step_callback('base_result', {
                'num1': x,
                'num2': y,
                'result': result,
                'message': f'Result: {x} × {y} = {result}'
            })
        return result
    
    # Make both strings same length by padding with zeros
    n = max(len(x_str), len(y_str))
    if n % 2 != 0:
        n += 1
    
    x_str = x_str.zfill(n)
    y_str = y_str.zfill(n)
    
    if step_callback:
        step_callback('normalize', {
            'num1': x,
            'num2': y,
            'num1_str': x_str,
            'num2_str': y_str,
            'n': n,
            'message': f'Normalized to {n} digits each'
        })
    
    # Split numbers into halves
    mid = n // 2
    
    a = int(x_str[:mid])
    b = int(x_str[mid:])
    c = int(y_str[:mid])
    d = int(y_str[mid:])
    
    if step_callback:
        step_callback('split', {
            'num1': x,
            'num2': y,
            'num1_str': x_str,
            'num2_str': y_str,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'mid': mid,
            'message': f'Split: x = {a}×10^{mid} + {b}, y = {c}×10^{mid} + {d}'
        })
    
    # Recursive calls
    if step_callback:
        step_callback('recursive_ac', {
            'a': a,
            'c': c,
            'message': f'Computing ac = {a} × {c}'
        })
    ac = karatsuba_multiply_visual(a, c, step_callback, delay)
    
    if step_callback:
        step_callback('recursive_ac_result', {
            'a': a,
            'c': c,
            'ac': ac,
            'message': f'ac = {a} × {c} = {ac}'
        })
    
    if step_callback:
        step_callback('recursive_bd', {
            'b': b,
            'd': d,
            'message': f'Computing bd = {b} × {d}'
        })
    bd = karatsuba_multiply_visual(b, d, step_callback, delay)
    
    if step_callback:
        step_callback('recursive_bd_result', {
            'b': b,
            'd': d,
            'bd': bd,
            'message': f'bd = {b} × {d} = {bd}'
        })
    
    if step_callback:
        step_callback('recursive_ad_bc', {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'message': f'Computing (a+b)(c+d) = ({a}+{b}) × ({c}+{d})'
        })
    ad_bc = karatsuba_multiply_visual(a + b, c + d, step_callback, delay) - ac - bd
    
    if step_callback:
        step_callback('recursive_ad_bc_result', {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'ad_bc': ad_bc,
            'message': f'(a+b)(c+d) - ac - bd = {ad_bc}'
        })
    
    # Combine results: 10^n * ac + 10^(n/2) * (ad + bc) + bd
    result = (10 ** n) * ac + (10 ** mid) * ad_bc + bd
    
    if step_callback:
        step_callback('combine', {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'ac': ac,
            'bd': bd,
            'ad_bc': ad_bc,
            'n': n,
            'mid': mid,
            'result': result,
            'message': f'Combining: 10^{n}×{ac} + 10^{mid}×{ad_bc} + {bd} = {result}'
        })
    
    return result

