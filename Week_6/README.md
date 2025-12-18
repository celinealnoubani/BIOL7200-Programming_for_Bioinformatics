# Week 6: Python Functions & Bioinformatics Applications

## Topics Covered
- Python function design
- Docstrings and type hints
- BLAST output parsing in Python
- BED and FASTA file processing
- Reverse complement calculation

## Scripts Developed

### 1. calnoubani3_q1.py - Drawing Triangles
Draws a diamond/triangle pattern using a specified character.

```python
def draw_triangle(char: str, size: int) -> None:
    """
    Draws a triangle of a given size using a specified character

    Arguments:
        char: character to build the triangle
        size: height of the triangle
    Returns:
        None (prints the triangle directly)
    """
    # Upper half
    for i in range(1, size//2 + 1):
        print(char * i)
    # Middle (if odd size)
    if size % 2 != 0:
        print(char * (size//2 + 1))
    # Lower half
    for i in range(size//2, 0, -1):
        print(char * i)
```

### 2. calnoubani3_q2.py - Parenthesis Matching
Checks if parentheses in a string are properly paired.

```python
def check_parenthesis(case: str) -> None:
    count = 0
    for char in case:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
            if count < 0:
                print("NOT PAIRED")
                return
    print("PAIRED" if count == 0 else "NOT PAIRED")
```

### 3. calnoubani3_q3.py - Gene Homolog Finder
Python implementation of Week 4's bash script - finds gene homologs using BLAST and BED files.

**Functions:**
| Function | Description |
|----------|-------------|
| `read_blast_file()` | Parse tblastn output, filter by identity/coverage |
| `read_bed_file()` | Parse BED annotations |
| `find_homologs()` | Match BLAST hits to gene coordinates |
| `read_fasta()` | Parse genome assembly |
| `rev_comp()` | Calculate reverse complement |

```python
def rev_comp(seq):
    """Get reverse complement of DNA sequence"""
    revs = {"A": "T", "T": "A", "C": "G", "G": "C"}
    rev_bases = [revs[base.upper()] for base in seq[::-1]]
    return "".join(rev_bases)
```

## Data Files

| File | Description |
|------|-------------|
| `Vc_blastout.txt` | tblastn results for V. cholerae |
| `Vibrio_cholerae_N16961.fna` | Genome assembly |
| `Vibrio_cholerae_N16961.bed` | Gene annotations |
| `HK_domain.faa` | Histidine kinase query protein |
| `Vc_outfile.txt` | Homolog gene sequences (FASTA) |

## Key Concepts

### Type Hints
```python
def function(param: str, size: int) -> None:
```

### Docstrings
```python
"""
Description of function

Arguments:
    param: description
Returns:
    description
"""
```

### File Parsing Pattern
```python
with open(file) as fin:
    for line in fin:
        fields = line.split()
        # process fields
```

## Learning Outcomes
- Write well-documented Python functions
- Use type hints for code clarity
- Parse bioinformatics file formats (BLAST, BED, FASTA)
- Implement reverse complement calculation
- Refactor bash scripts to Python
