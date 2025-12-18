# Week 11: Read Mapping & Consensus Sequences

## Topics Covered
- Read mapping with minimap2
- Consensus sequence generation
- Subprocess management in Python
- Complete NGS analysis pipeline

## Main Script: map_consensus.py

End-to-end pipeline for mapping reads and generating consensus sequences.

```python
#!/usr/bin/env python3
import argparse
import subprocess
from magnumopus.sam import SAM

def parse_args():
    parser = argparse.ArgumentParser(
        description="Map reads and generate consensus sequence"
    )
    parser.add_argument('-1', '--read1', required=True)
    parser.add_argument('-2', '--read2', required=True)
    parser.add_argument('-r', '--ref', required=True)
    parser.add_argument('-s', '--seq_name', help='Specific sequence name')
    return parser.parse_args()
```

## Pipeline Steps

### 1. Read Mapping with minimap2
```python
def run_minimap2(ref_path, read1_path, read2_path):
    cmd = [
        'minimap2',
        '-ax', 'sr',    # Short-read mode
        '-B', '0',      # Mismatch penalty 0
        '-k', '10',     # K-mer size 10
        ref_path,
        read1_path,
        read2_path
    ]
    subprocess.run(cmd, stdout=sam_file, check=True)
```

### 2. SAM Parsing
```python
sam = SAM.from_sam(sam_path)
```

### 3. Consensus Generation
```python
# Get consensus for specific sequence
consensus = sam.consensus(seq_name)

# Or get consensus for best mapping
consensus = sam.best_consensus()
```

### 4. FASTA Output
```python
def print_fasta(header, sequence):
    print(f">{header}")
    for i in range(0, len(sequence), 80):
        print(sequence[i:i+80])
```

## Usage

```bash
python map_consensus.py \
    -1 reads_R1.fastq \
    -2 reads_R2.fastq \
    -r reference.fna \
    -s "sequence_name"
```

## Data Files

| File | Description |
|------|-------------|
| `ERR11767307_1_vs_16S.sam` | Example SAM output |
| `data/` | Input FASTQ and reference files |

## minimap2 Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `-ax sr` | - | Short-read preset |
| `-B 0` | 0 | Mismatch penalty |
| `-k 10` | 10 | K-mer size |

## SAM Class Extension

Building on Week 10, the SAM class now includes:
- `from_sam()`: Class method for file parsing
- `consensus()`: Generate consensus for a reference
- `best_consensus()`: Get consensus from best mapping

## Module Structure
```
magnumopus/
├── __init__.py
├── sam.py          # SAM/Read classes + consensus
└── (other modules)
```

## Key Concepts

### Subprocess Management
```python
subprocess.run(cmd, stdout=file, stderr=subprocess.PIPE, check=True)
```

### Error Handling
```python
try:
    subprocess.run(cmd, check=True)
except FileNotFoundError:
    print("minimap2 not found")
    sys.exit(1)
```

## Learning Outcomes
- Integrate external tools (minimap2) with Python
- Build complete NGS analysis pipelines
- Generate consensus sequences from alignments
- Use subprocess for command-line tool integration
- Design command-line interfaces with argparse
