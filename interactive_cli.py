"""
Interactive Command-Line Interface for Divide and Conquer Algorithms
Works without tkinter
"""

import os
import time
from algorithms import (
    Point,
    closest_pair_divide_conquer,
    closest_pair_brute_force,
    karatsuba_multiply,
    standard_multiply
)


def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70 + "\n")


def list_files(directory, file_type):
    """List available input files"""
    files = []
    if os.path.exists(directory):
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.txt'):
                files.append((filename, os.path.join(directory, filename)))
    return files


def display_menu():
    """Display main menu"""
    print_header("DIVIDE AND CONQUER ALGORITHMS")
    print("1. Closest Pair of Points")
    print("2. Integer Multiplication (Karatsuba)")
    print("3. Run Demo (Process Sample Files)")
    print("4. Exit")
    print("\n" + "-" * 70)


def process_closest_pair():
    """Process closest pair algorithm"""
    clear_screen()
    print_header("CLOSEST PAIR OF POINTS")
    
    # List available files
    files = list_files("inputs/closest_pair", "closest pair")
    
    if not files:
        print("No input files found in inputs/closest_pair/")
        print("Run: python3 input_generator.py")
        input("\nPress Enter to continue...")
        return
    
    print("Available files:")
    for i, (filename, filepath) in enumerate(files, 1):
        print(f"  {i}. {filename}")
    
    try:
        choice = input("\nSelect file number (or 'b' to go back): ").strip()
        if choice.lower() == 'b':
            return
        
        file_idx = int(choice) - 1
        if file_idx < 0 or file_idx >= len(files):
            print("Invalid selection!")
            input("\nPress Enter to continue...")
            return
        
        filename, filepath = files[file_idx]
        
        # Load points
        print(f"\nLoading {filename}...")
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        num_points = int(lines[0].strip())
        points = []
        for i in range(1, num_points + 1):
            x, y = map(float, lines[i].strip().split())
            points.append(Point(x, y))
        
        print(f"Loaded {num_points} points")
        
        # Run algorithm
        print("\nRunning divide and conquer algorithm...")
        start_time = time.time()
        distance, pair = closest_pair_divide_conquer(points)
        execution_time = (time.time() - start_time) * 1000
        
        # Results
        print_header("RESULTS")
        print(f"Number of Points: {num_points}")
        print(f"Closest Distance: {distance:.6f}")
        print(f"Point 1: ({pair[0].x:.2f}, {pair[0].y:.2f})")
        print(f"Point 2: ({pair[1].x:.2f}, {pair[1].y:.2f})")
        print(f"Execution Time: {execution_time:.4f} ms")
        print(f"Time per Point: {execution_time/num_points:.6f} ms")
        
        # Compare with brute force if small enough
        if num_points <= 100:
            print("\nComparing with brute force...")
            start_brute = time.time()
            brute_dist, brute_pair = closest_pair_brute_force(points)
            brute_time = (time.time() - start_brute) * 1000
            speedup = brute_time / execution_time if execution_time > 0 else 0
            print(f"Brute Force Time: {brute_time:.4f} ms")
            print(f"Speedup: {speedup:.2f}x")
        
        input("\nPress Enter to continue...")
        
    except ValueError:
        print("Invalid input!")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input("\nPress Enter to continue...")


def process_integer_multiplication():
    """Process integer multiplication algorithm"""
    clear_screen()
    print_header("INTEGER MULTIPLICATION (KARATSUBA)")
    
    # List available files
    files = list_files("inputs/integer_multiplication", "integer multiplication")
    
    if not files:
        print("No input files found in inputs/integer_multiplication/")
        print("Run: python3 input_generator.py")
        input("\nPress Enter to continue...")
        return
    
    print("Available files:")
    for i, (filename, filepath) in enumerate(files, 1):
        print(f"  {i}. {filename}")
    
    try:
        choice = input("\nSelect file number (or 'b' to go back): ").strip()
        if choice.lower() == 'b':
            return
        
        file_idx = int(choice) - 1
        if file_idx < 0 or file_idx >= len(files):
            print("Invalid selection!")
            input("\nPress Enter to continue...")
            return
        
        filename, filepath = files[file_idx]
        
        # Load numbers
        print(f"\nLoading {filename}...")
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
        
        # Run algorithms
        print("\nRunning Karatsuba algorithm...")
        start_karatsuba = time.time()
        karatsuba_result = karatsuba_multiply(num1, num2)
        karatsuba_time = (time.time() - start_karatsuba) * 1000
        
        print("Running standard multiplication...")
        start_standard = time.time()
        standard_result = standard_multiply(num1, num2)
        standard_time = (time.time() - start_standard) * 1000
        
        # Verify correctness
        is_correct = (karatsuba_result == standard_result)
        
        # Results
        print_header("RESULTS")
        print(f"Input Size: {digits1} × {digits2} digits")
        print(f"\nKaratsuba Algorithm:")
        print(f"  Time: {karatsuba_time:.4f} ms")
        print(f"  Complexity: O(n^log2(3)) ≈ O(n^1.585)")
        print(f"\nStandard Multiplication:")
        print(f"  Time: {standard_time:.4f} ms")
        print(f"  Complexity: O(n²)")
        
        if standard_time > 0 and karatsuba_time > 0:
            speedup = standard_time / karatsuba_time if karatsuba_time > 0 else 0
            print(f"\nSpeedup: {speedup:.2f}x")
        
        print(f"\nCorrectness: {'✓ CORRECT' if is_correct else '✗ INCORRECT'}")
        print(f"\nResult (first 100 digits): {str(karatsuba_result)[:100]}...")
        print(f"Result (last 20 digits): ...{str(karatsuba_result)[-20:]}")
        
        input("\nPress Enter to continue...")
        
    except ValueError:
        print("Invalid input!")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"Error: {e}")
        input("\nPress Enter to continue...")


def run_demo():
    """Run demo on sample files"""
    clear_screen()
    print_header("RUNNING DEMO")
    print("This will process sample files from both algorithms...")
    input("\nPress Enter to start...")
    
    # Import and run the demo
    import run_demo
    run_demo.main()
    
    input("\nPress Enter to return to menu...")


def main():
    """Main interactive loop"""
    while True:
        clear_screen()
        display_menu()
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            process_closest_pair()
        elif choice == '2':
            process_integer_multiplication()
        elif choice == '3':
            run_demo()
        elif choice == '4':
            print("\nThank you for using Divide and Conquer Algorithms!")
            break
        else:
            print("Invalid choice! Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

