#!/usr/bin/env python3

import argparse
from magnumopus import ispcr, needleman_wunsch

# Compute reverse complement
def reverse_complement(sequence: str) -> str:
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement.get(base, base) for base in reversed(sequence))

# Clean sequence of headers
def clean_sequence(sequence: str) -> str:
    return "".join(line for line in sequence.splitlines() if not line.startswith(">"))

def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="Perform in-silico PCR on two assemblies and align the amplicons.")
    parser.add_argument("-1", "--assembly1", required=True, help="Path to the first assembly file")
    parser.add_argument("-2", "--assembly2", required=True, help="Path to the second assembly file")
    parser.add_argument("-p", "--primers", required=True, help="Path to the primer file")
    parser.add_argument("-m", "--max_amplicon_size", type=int, required=True, help="Maximum amplicon size for isPCR")
    parser.add_argument("--match", type=int, required=True, help="Match score to use in alignment")
    parser.add_argument("--mismatch", type=int, required=True, help="Mismatch penalty to use in alignment")
    parser.add_argument("--gap", type=int, required=True, help="Gap penalty to use in alignment")
    args = parser.parse_args()

    # Perform isPCR on both assemblies
    amplicon1 = clean_sequence(ispcr(args.primers, args.assembly1, args.max_amplicon_size))
    amplicon2 = clean_sequence(ispcr(args.primers, args.assembly2, args.max_amplicon_size))
    
    # Check both orientations for the best alignment
    forward_aln, forward_score = needleman_wunsch(amplicon1, amplicon2, args.match, args.mismatch, args.gap)
    rev_comp_amplicon2 = reverse_complement(amplicon2)
    reverse_aln, reverse_score = needleman_wunsch(amplicon1, rev_comp_amplicon2, args.match, args.mismatch, args.gap)

    # Choose best alignment based on score
    if forward_score >= reverse_score:
        best_alignment, best_score = forward_aln, forward_score
    else:
        best_alignment, best_score = reverse_aln, reverse_score

    # Print alignment & score
    print(">Assembly 1 Amplicon Alignment")
    print(best_alignment[0])
    print("\n>Assembly 2 Amplicon Alignment (or Reverse Complement)")
    print(best_alignment[1])
    print(f"\nAlignment Score: {best_score}")

if __name__ == "__main__":
    main()

