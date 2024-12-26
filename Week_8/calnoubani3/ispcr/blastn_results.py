#!/usr/bin/env python3

import subprocess

def run_blastn(primer_file: str, assembly_file: str) -> str:
    """
    Runs blastn using the given primer and assembly files, saving the output to a file.
    """
    output_file = "blast_output.txt"
    blastn_command = [
        "blastn",
        "-query", primer_file,
        "-subject", assembly_file,
        "-task", "blastn-short",
        "-outfmt", "6 std qlen",
        "-out", output_file
    ]
    subprocess.run(blastn_command)
    return output_file

def filter_hits(blast_output_file: str) -> list[list[str]]:
    """
    Filters blastn hits to keep only those w/ full length matches and at least 80% identity.
    """
    filtered_hits = []
    with open(blast_output_file, "r") as file:
        for line in file:
            columns = line.strip().split("\t")
            percent_identity = float(columns[2])
            alignment_length = int(columns[3])
            query_length = int(columns[12])
            
            if alignment_length == query_length and percent_identity >= 80.0:
                filtered_hits.append(columns)
    return filtered_hits

def step_one(primer_file: str, assembly_file: str) -> list[list[str]]:
    """
    Executes step one: Runs blastn and filters the output to identify primer annealing locations.
    """
    blast_output_file = run_blastn(primer_file, assembly_file)
    filtered_hits = filter_hits(blast_output_file)
    return sorted(filtered_hits, key=lambda x: (x[1], int(x[8]), int(x[9])))