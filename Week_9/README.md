# Week 9: Expanding the Magnumopus Package

## Topics Covered
- Building on existing Python packages
- Needleman-Wunsch global sequence alignment algorithm
- Amplicon alignment and analysis
- Complete in-silico PCR pipeline
- Package testing and validation

## Module: magnumopus

Extended bioinformatics package for PCR simulation and sequence analysis.

## Needleman-Wunsch Algorithm Implementation

The centerpiece of this week is a complete implementation of the **Needleman-Wunsch global sequence alignment algorithm** in `magnumopus/nw.py`.

### Algorithm Overview

Needleman-Wunsch is a dynamic programming algorithm that finds the optimal global alignment between two sequences. It guarantees the best possible alignment by exploring all possible alignments systematically.

### How It Works

**1. Matrix Initialization**
```
        -     C     T     T
  -     0    -1    -2    -3
  C    -1     ?     ?     ?
  T    -2     ?     ?     ?
```
- Create an (n+1) × (m+1) scoring matrix
- First row/column filled with cumulative gap penalties

**2. Matrix Filling (Dynamic Programming)**

For each cell, compute three possible scores:
- **Diagonal**: Previous cell + match/mismatch score (characters align)
- **Up**: Cell above + gap penalty (gap in sequence B)
- **Left**: Cell left + gap penalty (gap in sequence A)

Take the maximum of these three options:
```python
score_matrix[i][j] = max(diag_score, up_score, left_score)
```

**3. Traceback**

Starting from the bottom-right cell, trace back to find the optimal path:
- Diagonal move → align both characters
- Up move → gap in sequence B (insert `-`)
- Left move → gap in sequence A (insert `-`)

### Implementation Details

```python
def needleman_wunsch(seq_a: str, seq_b: str, match: int, mismatch: int, gap: int) -> tuple[tuple[str, str], int]:
    # Initialize scoring matrix with gap penalties
    n, m = len(seq_a) + 1, len(seq_b) + 1
    score_matrix = [[0] * m for _ in range(n)]

    for i in range(n):
        score_matrix[i][0] = i * gap  # Gap penalties for first column
    for j in range(m):
        score_matrix[0][j] = j * gap  # Gap penalties for first row

    # Fill matrix using dynamic programming
    for i in range(1, n):
        for j in range(1, m):
            if seq_a[i-1] == seq_b[j-1]:
                diag_score = score_matrix[i-1][j-1] + match
            else:
                diag_score = score_matrix[i-1][j-1] + mismatch
            up_score = score_matrix[i-1][j] + gap
            left_score = score_matrix[i][j-1] + gap
            score_matrix[i][j] = max(diag_score, up_score, left_score)

    # Traceback to build aligned sequences
    # ... returns aligned sequences and final score
```

### Usage Example

```python
import magnumopus

seq1 = "CTTCTCGTCGGTCTCGTGGTTCGGGAAC"
seq2 = "CTTTCATCCACTTCGTTGCCCGGGAAC"

alignment, score = magnumopus.needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-1)

print(alignment[0])  # CTTCTCGT-CGGTCTCGTGGTTCGGGAAC
print(alignment[1])  # CTT-TCATCCACT-TCGTTGCCCGGGAAC
print(f"Score: {score}")
```

### Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| `match` | Score for matching characters | +1 |
| `mismatch` | Penalty for mismatching characters | -1 |
| `gap` | Penalty for inserting a gap | -1 or -2 |

## Amplicon Alignment Pipeline

`amplicon_align.py` combines isPCR with Needleman-Wunsch to align amplicons from two different genome assemblies.

### Pipeline Flow
```
Assembly 1 ──→ isPCR ──→ Amplicon 1 ──┐
                                      ├──→ Needleman-Wunsch ──→ Alignment
Assembly 2 ──→ isPCR ──→ Amplicon 2 ──┘
```

### Features
- Performs isPCR on both assemblies using the same primers
- Aligns resulting amplicons using Needleman-Wunsch
- Automatically checks both forward and reverse complement orientations
- Selects the best alignment based on score

### Command-Line Usage
```bash
python amplicon_align.py \
    -1 assembly1.fna \
    -2 assembly2.fna \
    -p primers.fna \
    -m 2000 \
    --match 1 --mismatch -1 --gap -1
```

## In-Silico PCR (isPCR)

### Usage Example (q1.py)
```python
import magnumopus

primer_file = "data/rpoD.fna"
assembly = "data/Pseudomonas_aeruginosa_PAO1.fna"
max_amp_size = 2000

amplicons = magnumopus.ispcr(primer_file, assembly, max_amp_size)
print(amplicons)
```

## Package Functions

| Function | Description |
|----------|-------------|
| `needleman_wunsch()` | Global sequence alignment using dynamic programming |
| `ispcr()` | Main in-silico PCR function |
| `find_primers()` | Locate primer binding sites |
| `predict_amplicons()` | Generate amplicon sequences |
| `filter_by_size()` | Filter by amplicon length |

## Module Structure
```
magnumopus/
├── __init__.py     # Package initialization & exports
├── nw.py           # Needleman-Wunsch alignment algorithm
├── ispcr.py        # In-silico PCR functions
└── utils.py        # Utility functions
```

## Data Files

| File | Description |
|------|-------------|
| `rpoD.fna` | RNA polymerase sigma factor primers |
| `Pseudomonas_aeruginosa_PAO1.fna` | P. aeruginosa genome |

## Scripts

| Script | Description |
|--------|-------------|
| `q1.py` | Test isPCR function |
| `q2.py` | Test Needleman-Wunsch alignment |
| `amplicon_align.py` | Full pipeline: isPCR + alignment |

## Learning Outcomes
- Implement dynamic programming algorithms for bioinformatics
- Understand global sequence alignment (Needleman-Wunsch)
- Build scoring matrices and perform traceback
- Extend existing Python packages with new functionality
- Design command-line tools for bioinformatics pipelines
