# Week 2: Shell Scripting & BLAST

## Topics Covered
- Bash shell scripting fundamentals
- FASTA file manipulation with sed
- BLAST sequence alignment (blastn-short)
- Finding perfect sequence matches

## Scripts Developed

### 1. change_headers.sh
Modifies FASTA headers by prepending the accession number.

```bash
#!/bin/bash
input_file="$1"
output_file="$2"
accession="${input_file%.*}"
sed "/^>/ s/^>/>${accession}_/" "$input_file" > "$output_file"
```

**Usage:** `./change_headers.sh input.fna output.fna`

### 2. find_perfect_matches.sh
Finds perfect BLAST matches (100% identity, full length) for CRISPR spacers.

```bash
#!/bin/bash
blastn -query "$1" -subject "$2" -task blastn-short -outfmt '6 qseqid sseqid pident length qlen' | \
awk '$3 == 100 && $4 == $5 && $5 == 28' > "$3"
```

**Usage:** `./find_perfect_matches.sh query.fna subject.fna output.txt`

## Data Files

| File | Description |
|------|-------------|
| `CRISPR_1f.fna` | CRISPR spacer sequences (28 bp) |
| `ERR430992.fna` | Metagenomic reads dataset 1 |
| `ERR431227.fna` | Metagenomic reads dataset 2 |
| `*_perfect_matches.txt` | Perfect match results |

## Key Concepts

### BLAST Parameters
- `-task blastn-short`: Optimized for sequences < 50 bp
- `-outfmt 6`: Tabular output format
- Fields: qseqid, sseqid, pident, length, qlen

### sed for FASTA Headers
- Pattern: `/^>/` matches header lines
- Substitution: `s/^>/>${prefix}_/` prepends text

## Results
- Identified perfect matches of CRISPR spacers in metagenomic data
- Demonstrated CRISPR-based detection of bacteriophage sequences

## Learning Outcomes
- Write reusable shell scripts with command-line arguments
- Use sed for text manipulation in bioinformatics files
- Run BLAST for short sequence searches
- Filter BLAST output using awk
