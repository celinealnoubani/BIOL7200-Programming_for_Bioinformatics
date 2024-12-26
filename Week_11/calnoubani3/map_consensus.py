#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path
from magnumopus.sam import SAM

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Map reads and generate consensus sequence")
    parser.add_argument('-1', '--read1', required=True, help='Path to first read file (FASTQ)')
    parser.add_argument('-2', '--read2', required=True, help='Path to second read file (FASTQ)')
    parser.add_argument('-r', '--ref', required=True, help='Path to reference sequences (FASTA)')
    parser.add_argument('-s', '--seq_name', help='Optional: specific sequence name to get consensus for')
    return parser.parse_args()

def run_minimap2(ref_path: str, read1_path: str, read2_path: str) -> str:
    """Run minimap2 and return path to SAM output"""
    # Create SAM filename based on input
    sam_path = Path(read1_path).stem + '_vs_' + Path(ref_path).stem + '.sam'
    
    # Build minimap2 command with required settings
    cmd = [
        'minimap2',
        '-ax', 'sr',        # Short-read mode
        '-B', '0',          # Mismatch penalty 0
        '-k', '10',         # K-mer size 10
        str(ref_path),      # Reference path
        str(read1_path),    # Read1 path
        str(read2_path)     # Read2 path
    ]
    
    # Run minimap2 and get output
    with open(sam_path, 'w') as sam_file:
        try:
            subprocess.run(cmd, stdout=sam_file, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running minimap2: {e.stderr.decode()}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("Error: minimap2 not found. Please ensure it's installed and in your PATH.", file=sys.stderr)
            sys.exit(1)
            
    return sam_path

def print_fasta(header: str, sequence: str):
    """Print sequence in FASTA format"""
    print(f">{header}")
    # Print sequence in lines of 80 characters
    for i in range(0, len(sequence), 80):
        print(sequence[i:i+80])

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Run minimap2 to align reads to reference
    sam_path = run_minimap2(args.ref, args.read1, args.read2)
    
    # Parse SAM file
    sam = SAM.from_sam(sam_path)
    
    # Get consensus sequence
    if args.seq_name:
        # Get consensus for specified sequence
        consensus = sam.consensus(args.seq_name)
        if not consensus:
            print(f"Error: No consensus found for sequence {args.seq_name}", file=sys.stderr)
            sys.exit(1)
        header = f"{args.seq_name}_consensus"
    else:
        # Get consensus for best mapping
        consensus = sam.best_consensus()
        if not consensus:
            print("Error: No consensus sequence found", file=sys.stderr)
            sys.exit(1)
        header = "best_mapping_consensus"
    
    # Print consensus in FASTA format
    print_fasta(header, consensus)

if __name__ == '__main__':
    main()