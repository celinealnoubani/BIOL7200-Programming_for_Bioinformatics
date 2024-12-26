#!/bin/bash

# Assign inputs to variables
query_file="$1"
subject_file="$2"
output_file="$3"


# Run BLAST
tblastn -query "$query_file" -subject "$subject_file" -outfmt '6 qseqid sseqid pident length' | \
awk '$3 > 30 && $4 >= 0.9*length($1)' > "$output_file"


# Count the number of perfect matches & print to stdout
echo "$(wc -l $output_file) matches found in $subject_file"






