# Week 4: Bash Scripting - Finding Gene Homologs

## Topics Covered
- Advanced bash scripting with loops
- Protein BLAST (tblastn)
- BED file parsing
- Finding gene homologs across bacterial genomes

## Main Script: calnoubani3.sh

Identifies genes containing protein domain homologs by combining tblastn results with BED annotations.

```bash
#!/usr/bin/env bash
query=$1      # Protein query (HK_domain.faa)
subject=$2    # Genome assembly (*.fna)
bedfile=$3    # Gene annotations (*.bed)
outfile=$4    # Output file

# Run tblastn with filtering (>30% identity, >90% query coverage)
tblastn -query $query -subject $subject -outfmt '6 std qlen' \
| awk '$3>30 && $4>0.9*$13' > $blast_tmp

# Find genes overlapping with BLAST hits
while read _ blast_seqid _ _ _ _ _ _ blast_start blast_stop _
do
    while read bed_seqid bed_start bed_stop gene orientation
    do
        if [[ $blast_seqid == $bed_seqid && \
              $blast_start -le $bed_stop && \
              $blast_stop -ge $bed_start ]]
        then
            echo $gene >> $gene_tmp
        fi
    done < $bedfile
done < $blast_tmp
```

## Organisms Analyzed

| Organism | Genome File | Annotation |
|----------|-------------|------------|
| *E. coli* K12 | `Escherichia_coli_K12.fna` | `*.bed` |
| *P. aeruginosa* PA14 | `Pseudomonas_aeruginosa_UCBPP-PA14.fna` | `*.bed` |
| *V. cholerae* N16961 | `Vibrio_cholerae_N16961.fna` | `*.bed` |
| *Wolbachia* | `Wolbachia.fna` | `*.bed` |

## Query Protein
- `HK_domain.faa`: Histidine Kinase domain - key component of two-component signaling systems in bacteria

## Key Concepts

### tblastn
- Searches protein query against translated nucleotide database
- Useful for finding gene homologs in unannotated genomes

### Overlap Detection
```bash
# Check if BLAST hit overlaps with BED feature
blast_start -le bed_stop && blast_stop -ge bed_start
```

### Filtering Criteria
- Percent identity > 30%
- Alignment length > 90% of query length

## Output Files
- `*_results`: Unique gene names containing HK domain homologs
- `*_results.tmp`: Intermediate files

## Learning Outcomes
- Write complex bash scripts with nested loops
- Use tblastn for protein-to-genome searches
- Parse and compare BED coordinates with BLAST hits
- Identify functional domain homologs across species
