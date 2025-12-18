# Week 1: Unix/Linux Fundamentals

## Topics Covered
- Linux command-line basics
- File navigation and manipulation
- Input/output redirection (stdout, stderr)
- BED file format introduction

## Skills Practiced

### File Operations
- Creating, copying, and moving files
- Viewing file contents
- Working with file permissions

### Redirection
- Standard output (`>`, `>>`)
- Standard error (`2>`)
- Combining streams

### BED File Manipulation
- Understanding BED format (chromosome, start, end, name, score, strand)
- Extracting and modifying columns
- Adding size calculations to genomic features

## Files

| File | Description |
|------|-------------|
| `ex1.bed` | Original BED file |
| `ex1_noheader.bed` | BED file with header removed |
| `ex1_sizes.bed` | BED file with feature sizes added |
| `ex1_unix.bed` | Unix-formatted BED file |
| `stdout.txt` | Captured standard output |
| `stderr.txt` | Captured standard error |
| `error.txt` | Error log file |

## Key Commands Learned
```bash
# File operations
cp, mv, rm, cat, head, tail

# Redirection
command > output.txt      # stdout to file
command 2> error.txt      # stderr to file
command &> both.txt       # both streams to file

# Text processing
cut, sort, awk
```

## Learning Outcomes
- Navigate Linux filesystem confidently
- Redirect command output to files
- Understand BED file format for genomic annotations
- Perform basic text processing on bioinformatics files
