# Week 10: SAM File Parsing

## Topics Covered
- SAM file format specification
- Object-oriented programming in Python
- CIGAR string parsing
- Read alignment analysis

## Module: magnumopus.sam

Implements a `Read` class for parsing and analyzing SAM alignment records.

### Read Class

```python
class Read:
    def __init__(self, line):
        fields = line.strip().split()
        self.qname = fields[0]   # Query name
        self.flag = int(fields[1])   # Bitwise flag
        self.rname = fields[2]   # Reference name
        self.pos = int(fields[3])    # 1-based position
        self.mapq = int(fields[4])   # Mapping quality
        self.cigar = fields[5]   # CIGAR string
        self.seq = fields[9]     # Sequence
        self.qual = fields[10]   # Quality scores
```

### Properties (Bitwise Flag Parsing)

| Property | Description | Flag |
|----------|-------------|------|
| `is_mapped` | Read is mapped | `0x4` |
| `is_forward` | Forward strand | `0x10` |
| `is_reverse` | Reverse strand | `0x10` |
| `is_primary` | Primary alignment | `0x100`, `0x800` |

```python
@property
def is_mapped(self):
    return not (self.flag & 0x4)

@property
def is_reverse(self):
    return bool(self.flag & 0x10)
```

### Methods

| Method | Description |
|--------|-------------|
| `base_at_pos(pos)` | Get base at reference position |
| `qual_at_pos(pos)` | Get quality at reference position |
| `mapped_seq()` | Get mapped portion of sequence |

### CIGAR String Parsing

```python
def base_at_pos(self, pos: int) -> str:
    cigar_pattern = re.findall(r'(\d+)([MIDNSHP=X])', self.cigar)

    for length, op in cigar_pattern:
        if op == 'M':    # Match/mismatch
            # Advance both ref and read
        elif op == 'D':  # Deletion in read
            # Advance ref only
        elif op == 'I':  # Insertion in read
            # Advance read only
        elif op == 'S':  # Soft clipping
            # Advance read only
```

## CIGAR Operations

| Op | Description | Reference | Read |
|----|-------------|-----------|------|
| M | Match/Mismatch | +length | +length |
| D | Deletion | +length | - |
| I | Insertion | - | +length |
| S | Soft clip | - | +length |

## Module Structure
```
magnumopus/
├── __init__.py
├── sam.py          # Read class
└── (other modules)
```

## Key Concepts

### Object-Oriented Design
- Class encapsulates SAM record data
- Properties for computed attributes
- Methods for position-based queries

### Bitwise Operations
```python
flag & 0x4      # Check if bit is set
not (flag & 0x4)    # Check if bit is unset
```

## Learning Outcomes
- Parse SAM file format
- Implement CIGAR string interpretation
- Use Python classes and properties
- Apply bitwise operations for flag parsing
- Navigate read alignments programmatically
