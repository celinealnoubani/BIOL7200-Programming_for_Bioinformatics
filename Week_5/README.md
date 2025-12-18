# Week 5: Introduction to Python

## Topics Covered
- Python fundamentals
- Reading files in Python
- String manipulation
- Sequence comparison and alignment visualization

## Main Script: calnoubani3_1.py

Compares two sequences from a FASTA file and visualizes matching positions.

```python
#!/usr/bin/env python3
import sys

fa_file = open(sys.argv[1])
contents = fa_file.readlines()

# Extract sequences (every other line after headers)
new_list = []
for i in range(1, len(contents), 2):
    new_list.append(contents[i].strip())

x, y = new_list
print(x)

# Print alignment visualization
counter = 0
for char in x:
    if char == y[counter]:
        print("|", end="")  # Match
    else:
        print(" ", end="")  # Mismatch
counter += 1

print()
print(y)
```

## Example Output
```
ATGCGATCGATCGATCG
||| ||||||  ||||||
ATGGGATCGAAGGATCG
```

## Files

| File | Description |
|------|-------------|
| `calnoubani3_1.py` | Sequence comparison script |
| `FASTA_file.fa` | Input FASTA with two sequences |

## Key Python Concepts

### File I/O
```python
file = open(filename)
contents = file.readlines()
file.close()
```

### Command-Line Arguments
```python
import sys
input_file = sys.argv[1]  # First argument
```

### String Operations
- `.strip()` - Remove whitespace
- `end=""` - Control print line endings
- Indexing: `string[i]`

## Learning Outcomes
- Write basic Python scripts
- Read and parse FASTA files
- Compare sequences character by character
- Create simple alignment visualizations
- Use command-line arguments in Python
