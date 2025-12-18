# BIOL 7200 - Programming for Bioinformatics

**Georgia Institute of Technology**

## Overview

This repository contains coursework for Programming for Bioinformatics, covering the progression from Unix/Linux fundamentals to building complete bioinformatics pipelines in Python. The course emphasizes practical skills for analyzing biological sequence data.

## Course Progression

| Week | Topic | Key Skills |
|------|-------|------------|
| [Week 1](./Week%201) | Unix/Linux Fundamentals | File operations, redirection, BED files |
| [Week 2](./Week_2) | Shell Scripting & BLAST | Bash scripts, sed, blastn-short |
| [Week 3](./Week_3) | Advanced BLAST Analysis | Pipeline construction, filtering |
| [Week 4](./Week_4) | Bash Scripting | tblastn, BED parsing, gene homologs |
| [Week 5](./Week_5) | Python Basics | File I/O, string manipulation |
| [Week 6](./Week_6) | Python Functions | Functions, docstrings, FASTA/BED parsing |
| [Week 7](./Week_7) | Data Visualization | pandas, matplotlib, epidemiological data |
| [Week 8](./Week_8) | Python Modules | Package development, in-silico PCR |
| [Week 9](./Week_9) | Package Extension | magnumopus module, amplicon analysis |
| [Week 10](./Week_10) | SAM File Parsing | OOP, CIGAR strings, Read class |
| [Week 11](./Week_11) | Read Mapping Pipeline | minimap2, consensus sequences |

---

## Technical Skills Developed

### Shell/Bash
- Unix command-line operations
- Shell scripting with loops and conditionals
- Text processing (sed, awk, grep)
- BLAST command-line tools

### Python
- File I/O and parsing (FASTA, BED, BLAST, SAM)
- Function design with type hints and docstrings
- Object-oriented programming (classes, properties)
- Package/module development
- Data analysis (pandas) and visualization (matplotlib)
- Subprocess integration for external tools

### Bioinformatics
- Sequence alignment (BLAST, minimap2)
- In-silico PCR simulation
- SAM/BAM file analysis
- Consensus sequence generation
- Gene homolog identification

---

## Major Projects

### In-Silico PCR Module (Weeks 8-9)
Python package for predicting PCR amplicons from primer sequences.

```python
import magnumopus
amplicons = magnumopus.ispcr(primers, genome, max_size)
```

### SAM Parser (Week 10)
Object-oriented SAM file parser with CIGAR string interpretation.

```python
from magnumopus.sam import Read
read = Read(sam_line)
base = read.base_at_pos(100)
```

### Read Mapping Pipeline (Week 11)
Complete pipeline integrating minimap2 alignment with consensus generation.

```bash
python map_consensus.py -1 R1.fq -2 R2.fq -r ref.fna
```

---

## Repository Structure

```
BIOL7200-Programming_for_Bioinformatics/
├── Week 1/                 # Unix fundamentals
├── Week_2/                 # Shell scripting & BLAST
├── Week_3/                 # Advanced BLAST
├── Week_4/                 # Bash scripting
├── Week_5/                 # Python basics
├── Week_6/                 # Python functions
├── Week_7/                 # Data visualization
├── Week_8/                 # Python modules (ispcr)
├── Week_9/                 # Package extension (magnumopus)
├── Week_10/                # SAM parsing
├── Week_11/                # Read mapping pipeline
└── README.md
```

---

## Tools & Technologies

### Command-Line Tools
- **BLAST** (blastn, tblastn) - Sequence alignment
- **minimap2** - Read mapping
- **sed/awk** - Text processing

### Python Libraries
- **pandas** - Data manipulation
- **matplotlib** - Visualization
- **argparse** - CLI development
- **subprocess** - External tool integration

### File Formats
- FASTA - Sequence data
- BED - Genomic annotations
- SAM - Sequence alignments
- BLAST tabular output

---

## Key Concepts

- **Pipeline Design**: Building reproducible analysis workflows
- **Modular Programming**: Creating reusable bioinformatics tools
- **File Format Parsing**: Working with standard bioinformatics formats
- **Algorithm Implementation**: In-silico PCR, consensus calling
- **Data Visualization**: Presenting biological data effectively

---

## Contact

Celine Alnoubani
Georgia Institute of Technology
