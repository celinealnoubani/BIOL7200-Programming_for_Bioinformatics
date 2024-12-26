#!/bin/bash

# Extract input & output file names
input_file="$1"
output_file="$2"

# Extract the accession number (filename w/o the extension)
accession="${input_file%.*}"

# Modify the headers & write to the output file
sed "/^>/ s/^>/>${accession}_/" "$input_file" > "$output_file"



