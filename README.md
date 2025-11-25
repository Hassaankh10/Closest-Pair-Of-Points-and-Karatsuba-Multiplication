# Divide and Conquer Algorithms Project

This project implements two divide and conquer algorithms with a Python GUI interface for visualization and analysis.

## Algorithms Implemented

1. **Closest Pair of Points** - Finds the two closest points in a 2D plane using divide and conquer (O(n log² n))
2. **Integer Multiplication (Karatsuba)** - Efficiently multiplies large integers using Karatsuba's algorithm (O(n^log₂(3)))

## Project Structure

```
.
├── algorithms.py              # Core algorithm implementations
├── algorithms_visual.py       # Step-by-step visualization versions
├── gui.py                     # Main GUI application
├── input_generator.py         # Generates random input files
├── interactive_cli.py         # Alternative CLI interface
├── run_demo.py                # Command-line demo script
├── test_algorithms.py         # Test suite
├── requirements.txt           # Python dependencies
├── inputs/
│   ├── closest_pair/          # 11 input files (10-1000 points)
│   └── integer_multiplication/ # 11 input files (10-500 digits)
├── README.md                  # This file
└── report.md                  # 3-page project report
```

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate Input Files

First, generate the input datasets:
```bash
python3 input_generator.py
```

This creates 20 input files:
- 10 files in `inputs/closest_pair/` (150-1000 points each)
- 10 files in `inputs/integer_multiplication/` (120-500 digits each)

### Run the Application

**Option 1: GUI Application (requires tkinter)**
```bash
python3 gui.py
```

**Option 2: Interactive CLI (works without tkinter)**
```bash
python3 interactive_cli.py
```

**Note:** If tkinter is not available, the GUI will show installation instructions. Use the interactive CLI instead.

### Using the Interface

1. **Closest Pair of Points Tab:**
   - Select an input file using "Browse" or "Quick Select"
   - Click "Run Algorithm" to find the closest pair
   - View results and visualization

2. **Integer Multiplication Tab:**
   - Select an input file using "Browse" or "Quick Select"
   - Click "Run Algorithm" to multiply the numbers
   - Compare Karatsuba vs Standard multiplication performance

## Features

- ✅ **Step-by-step visualization** - Watch algorithms work in real-time
- ✅ **Interactive file selection** - Browse or quick-select from generated files
- ✅ **Real-time visualization** - See points and algorithm steps graphically
- ✅ **Performance metrics** - Execution time and speedup comparisons
- ✅ **Correctness verification** - Automatic validation of results
- ✅ **Modern GUI** - Beautiful, elegant interface with color-coded steps
- ✅ **Multiple interfaces** - GUI, CLI, and demo scripts available

## Input File Format

### Closest Pair Format
```
n
x1 y1
x2 y2
...
xn yn
```

### Integer Multiplication Format
```
number1
number2
```

## Testing

All algorithms have been tested on 10 different input files each, with all inputs exceeding 100 elements. Results show:
- 100% correctness across all test cases
- Significant performance improvements for larger inputs
- Proper handling of edge cases

## Report

See `report.md` for the complete 3-page project report including:
- Abstract
- Introduction
- System architecture and design
- Experimental setup
- Results and discussion
- Conclusion
- References

## Requirements

- Python 3.7+
- matplotlib >= 3.5.0
- tkinter (usually included with Python, but may need separate installation)

### Installing tkinter

**Note:** tkinter cannot be installed via pip. It must be installed through your system package manager:

- **macOS:** `brew install python-tk` (or `brew install python-tk@3.14` for specific Python version)
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **Windows:** tkinter is usually included with Python installations
- **Fedora/RHEL:** `sudo dnf install python3-tkinter`

**If tkinter is not available**, you can still use the project with:
- `interactive_cli.py` - Full-featured command-line interface
- `run_demo.py` - Quick demo script

