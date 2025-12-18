# Week 8: Python Modules - In-Silico PCR

## Topics Covered
- Python module development
- Package structure and imports
- In-silico PCR implementation
- BLAST integration for primer matching

## Module: ispcr

Implements in-silico PCR to predict amplicons from primer sequences against genome assemblies.

### Module Structure
```
ispcr/
├── __init__.py
└── core functions
```

### Usage Example (q1.py)
```python
from ispcr import step_one

sorted_good_hits = step_one(
    primer_file="data/general_16S_515f_806r.fna",
    assembly_file="data/Vibrio_cholerae_N16961.fna"
)

for hit in sorted_good_hits:
    print(hit)
```

## In-Silico PCR Workflow

1. **Primer Input**: Load forward and reverse primer sequences
2. **BLAST Search**: Find primer binding sites in genome
3. **Hit Filtering**: Filter by identity and alignment length
4. **Amplicon Prediction**: Identify regions between primer pairs
5. **Size Filtering**: Return amplicons within expected size range

## Data Files

| File | Description |
|------|-------------|
| `general_16S_515f_806r.fna` | Universal 16S rRNA primers |
| `Vibrio_cholerae_N16961.fna` | V. cholerae genome assembly |
| `blast_output.txt` | BLAST results |

## Key Concepts

### Module Imports
```python
from ispcr import step_one
from ispcr import function_name
```

### Package Development
- `__init__.py` defines public API
- Functions organized by workflow step
- Reusable across different genomes/primers

## Scripts

| Script | Description |
|--------|-------------|
| `q1.py` | Test step_one function |
| `q2.py` | Test additional functions |
| `q3.py` | Full pipeline test |

## Learning Outcomes
- Create Python packages with proper structure
- Design modular, reusable bioinformatics tools
- Implement in-silico PCR algorithms
- Use BLAST programmatically from Python
- Test modules with example scripts
