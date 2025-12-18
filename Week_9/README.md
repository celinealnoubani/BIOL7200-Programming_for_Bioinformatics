# Week 9: Expanding the Magnumopus Package

## Topics Covered
- Building on existing Python packages
- Amplicon alignment and analysis
- Complete in-silico PCR pipeline
- Package testing and validation

## Module: magnumopus

Extended bioinformatics package for PCR simulation and sequence analysis.

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
| `ispcr()` | Main in-silico PCR function |
| `find_primers()` | Locate primer binding sites |
| `predict_amplicons()` | Generate amplicon sequences |
| `filter_by_size()` | Filter by amplicon length |

## Amplicon Alignment Script

`amplicon_align.py` - Aligns predicted amplicons for validation.

## Data Files

| File | Description |
|------|-------------|
| `rpoD.fna` | RNA polymerase sigma factor primers |
| `Pseudomonas_aeruginosa_PAO1.fna` | P. aeruginosa genome |

## Module Structure
```
magnumopus/
├── __init__.py     # Package initialization
├── ispcr.py        # In-silico PCR functions
└── utils.py        # Utility functions
```

## Key Concepts

### Complete PCR Simulation
```python
# Single function call for full pipeline
amplicons = magnumopus.ispcr(
    primers,      # Primer FASTA
    genome,       # Target genome
    max_size      # Maximum amplicon size
)
```

### Package Extension
- Build on Week 8's ispcr module
- Add new functionality incrementally
- Maintain backward compatibility

## Scripts

| Script | Description |
|--------|-------------|
| `q1.py` | Test ispcr function |
| `q2.py` | Test additional features |
| `amplicon_align.py` | Align amplicons |

## Learning Outcomes
- Extend existing Python packages
- Implement complete bioinformatics pipelines
- Design clean APIs for complex workflows
- Test package functionality systematically
