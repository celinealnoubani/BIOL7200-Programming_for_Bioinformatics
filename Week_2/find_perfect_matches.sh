#!/bin/bash

# Assign inputs to variables
query_file="$1"
subject_file="$2"
output_file="$3"


# Run BLAST
blastn -query "$query_file" -subject "$subject_file" -task blastn-short -outfmt '6 qseqid sseqid pident length qlen' | \
awk '$3 == 100 && $4 == $5 && $5 == 28' > "$output_file"


# Count the number of perfect matches & print to stdout
perfect_match=$(wc -l < "$output_file")
echo "Number of perfect matches: $perfect_match"




