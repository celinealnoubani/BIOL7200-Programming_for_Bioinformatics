#!/usr/bin/env python3

import sys

blastfile = sys.argv[1]
bedfile = sys.argv[2]
assembly = sys.argv[3]
outfile = sys.argv[4]

# Read BLAST file & extract hits
def read_blast_file(file):
    hits = []
    with open(file) as fin:
        for line in fin:
            _, sid, pcnt, matchlen, _, _, _, _, sstart, send, _, _, qlen = line.split()
            pcnt = float(pcnt)
            matchlen = int(matchlen)
            sstart = int(sstart)
            send = int(send)
            qlen = int(qlen)

            if pcnt > 30 and matchlen > 0.9 * qlen:
                hits.append((sid, sstart, send))
    return hits

hits = read_blast_file(blastfile)

# Read BED file & extract features
def read_bed_file(file):
    feats = []
    with open(file) as fin:
        for line in fin:
            bed_sid, bed_start, bed_end, gene, _, strand = line.split()
            bed_start = int(bed_start)
            bed_end = int(bed_end)
            feats.append((bed_sid, bed_start, bed_end, gene, strand))
    
    return feats

feats = read_bed_file(bedfile)

# Find homologous genes from BLAST hits and BED features
def find_homologs(blast_hits, bed_feats):
    homologs = []
    seen_genes = set()  
    for blast_sid, blast_sstart, blast_send in blast_hits:
        for bed_sid, bed_start, bed_end, gene, strand in bed_feats:
            if blast_sid != bed_sid:
                continue

            if blast_sstart <= bed_start or blast_send <= bed_start:
                break

            if (blast_sstart > bed_start
                and blast_sstart <= bed_end
                and blast_send > bed_start
                and blast_send <= bed_end
            ):
                if gene not in seen_genes: 
                    homologs.append((bed_sid, bed_start, bed_end, gene, strand))
                    seen_genes.add(gene) 
                break
    return homologs

homologs = find_homologs(hits, feats)

# Read FASTA assembly file into a dictionary
def read_fasta(fasta_file):
    sequences = {}
    with open(fasta_file) as fin:
        seq_lines = []
        for line in fin:
            if line[0] == ">":
                if seq_lines:
                    sequences[header] = "".join(seq_lines)
                    seq_lines = []
                header = line.split()[0][1:]
                continue
            seq_lines.append(line.strip())
        sequences[header] = "".join(seq_lines)
    return sequences

assembly_sequences = read_fasta(assembly)

# Get reverse complement of DNA sequence
def rev_comp(seq):
    revs = {"A": "T", "T": "A", "C": "G", "G": "C"}
    rev_bases = [revs[base.upper()] for base in seq[::-1]]
    return "".join(rev_bases)

#Write homolog gene sequences to output file
outcontents = []
for bed_sid, bed_start, bed_end, gene, strand in homologs:
    if strand == "+":
        seq = assembly_sequences[bed_sid][bed_start-1:bed_end]
    else:
        seq = rev_comp(assembly_sequences[bed_sid][bed_start-1:bed_end])
    outcontents += [f">{gene}", seq]
    
with open(outfile, 'w') as fout:
    fout.write("\n".join(outcontents) + "\n")

# Print the number of homologs found
print(f"Number of unique homologs: {len(homologs)}")
