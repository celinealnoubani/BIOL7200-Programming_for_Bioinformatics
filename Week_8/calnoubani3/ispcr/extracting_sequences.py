#!/usr/bin/env python3

import subprocess
import tempfile

def step_three(hit_pairs: list[tuple[list[str]]], assembly_file: str) -> str:
    """
    Extracts amplified sequences based on hit pairs.
    """
    bed_content = ""
    for pair in hit_pairs:
        contig = pair[0][1]
        start = pair[0][9]
        end = str(int(pair[1][9]) - 1) 
        bed_content += f"{contig}\t{start}\t{end}\n"
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.bed') as bed_file:
        bed_file.write(bed_content)
    
    result = subprocess.run(["seqtk", "subseq", assembly_file, bed_file.name], capture_output=True, text=True)
    return result.stdout