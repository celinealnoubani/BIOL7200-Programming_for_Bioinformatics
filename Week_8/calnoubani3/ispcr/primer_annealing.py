#!/usr/bin/env python3

def identify_amplicons(sorted_hits: list[str], max_amplicon_size: int) -> list[tuple[list[str]]]:
    """
    Identifies pairs of primer annealing sites that are less than max_amplicon_size apart
    & are pointing towards each other.
    """
    amplicons = []
    n = len(sorted_hits)
    
    for i in range(n):
        primer_1 = sorted_hits[i]
        start_1, end_1 = int(primer_1[8]), int(primer_1[9])
        
        for j in range(i + 1, n):
            primer_2 = sorted_hits[j]
            start_2, end_2 = int(primer_2[8]), int(primer_2[9])
            
            # Checks if primers are pointing towards each other and distance is within max_amplicon_size
            if ((start_1 < end_1 and start_2 > end_2) or (start_1 > end_1 and start_2 < end_2)) and abs(start_2 - start_1) <= max_amplicon_size:
                amplicons.append((primer_1, primer_2))
    
    return amplicons

def step_two(sorted_hits: list[str], max_amplicon_size: int) -> list[tuple[list[str]]]:
    """
    Executes step two: identifies pairs of primer annealing sites that would make an amplicon.
    """
    return identify_amplicons(sorted_hits, max_amplicon_size)
