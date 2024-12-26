#!/usr/bin/env bash

query=$1
subject=$2
bedfile=$3
outfile=$4

# Make tmp files
blast_tmp=$(mktemp)
gene_tmp=$(mktemp)

# Run BLAST (only keep hits with >30% id & 90% length)
tblastn -query $query -subject $subject -outfmt '6 std qlen' \
| awk '$3>30 && $4>0.9*$13' > $blast_tmp

# Loop over BLAST hits
while read _ blast_seqid _ _ _ _ _ _ blast_start blast_stop _
do
	# Loop over BED file
    	while read bed_seqid bed_start bed_stop gene orientation
    	do
        	# Check if we're on the same contig and the BLAST hit overlaps w/ the BED feature
        	if [[ $blast_seqid == $bed_seqid && $blast_start -le $bed_stop && $blast_stop -ge $bed_start ]]
        	then
            		echo $gene >> $gene_tmp
        	fi
    	done < $bedfile
done < $blast_tmp

sort -u $gene_tmp > $outfile

rm $blast_tmp
rm $gene_tmp

echo "Number of homolog matches in $bedfile: "$(wc -l < $outfile)""
