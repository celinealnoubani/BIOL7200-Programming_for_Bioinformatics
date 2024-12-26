#!/usr/bin/env python3

import re

class Read:
    def __init__(self, sam_line: str):
        (qname, flag, rname, pos, mapq, cigar, rnext, pnext, tlen, seq, qual, *tags) = sam_line.strip().split("\t")

        # store basic properties of the read
        self.qname: str = qname
        self.flag: int = int(flag)
        self.rname: str = rname
        self.pos: str = int(pos)
        self.mapq: str = int(mapq)
        self.cigar: str = cigar
        self.rnext: str = rnext
        self.pnext: str = int(pnext)
        self.tlen: str = int(tlen)
        self.seq: str = seq
        self.qual: str = qual
        self.tags: list[str] = tags

        # score mapping properties based on flag
        self.is_mapped: bool = not bool(self.flag & 4) 
        self.is_forward: bool = not bool(self.flag & 16)
        self.is_reverse: bool = bool(self.flag & 16)
        self.is_primary: bool = not (bool(self.flag & 256) or bool(self.flag & 2048)) 

        # add data for mapped reads only
        self.cigar_bits: tuple[tuple[int, str]] = None
        self.mapped_len: int = None
        
        if self.is_mapped:
            self.cigar_bits = tuple([(int(n), cig) for n, cig in re.findall(r"(\d+)([A-Z])", self.cigar)])
            self.mapped_len = sum([n for n, cig in self.cigar_bits if cig in {"M", "D"}])

    def read_idx_at_pos(self, pos: int) -> list[None|int]:
        if not self.is_mapped:
            return []
        
        # adjust by read start
        pos -= self.pos
        if pos < 0: # If read mapped to the right of requested location
            return []

        # Check if the requested position is right of our read
        if pos >= self.mapped_len:
            return []
        
        cigar_bits = re.findall(r"(\d+)([A-Z])", self.cigar)
        # pad position based on cigar
        pad = 0
        mapped_count = 0
        for n, (size, cig_type) in enumerate(cigar_bits):
            size = int(size)
            if cig_type in {"S", "H", "I"}:
                pad += size
                continue
            if mapped_count + size >= pos+1:
                if cig_type == "M":
                    # pad remaining
                    pad += (pos-mapped_count)
                    break
                if cig_type == "D":
                    return []
            else:
                if cig_type == "M":
                    mapped_count += size
                    pad += size
                if cig_type == "D":
                    mapped_count += size

        # Check if next bases are insertion
        if mapped_count + size == pos+1:
            if n+1 != len(cigar_bits):
                size, cig_type = cigar_bits[n+1]
                size = int(size)
                if cig_type == "I":
                    return [i for i in range(pad, pad+size+1)]

        return [pad]

    def mapped_seq(self) -> str:
        if not self.is_mapped:
            return ""

        idx = 0 
        bases = [] 
        for n, cig in self.cigar_bits:
            if cig == "S":
                idx += n
            elif cig == "D":
                bases += ["-"]*n
            elif cig in {"M", "I"}:
                bases += [self.seq[i] for i in range(idx, idx+n)]
                idx += n

        return "".join(bases)

    def base_at_pos(self, pos: int) -> str:
        idx = self.read_idx_at_pos(pos)
        return "".join([self.seq[i] for i in idx])

    def qual_at_pos(self, pos: int) -> str:
        idx = self.read_idx_at_pos(pos)
        return "".join([self.qual[i] for i in idx])

class SAM:
    """Class to store and process SAM format alignments"""
    def __init__(self):
        self.reads: list[Read] = []
        self.references: set[str] = set()
        
    @classmethod
    def from_sam(cls, sam_file: str) -> 'SAM':
        """Create SAM instance from SAM file, storing only primary mappings"""
        sam = cls()
        
        with open(sam_file) as f:
            for line in f:
                if line.startswith('@'):  # Header line
                    if line.startswith('@SQ'):  # Reference sequence
                        fields = line.strip().split('\t')
                        for field in fields:
                            if field.startswith('SN:'):
                                sam.references.add(field[3:])
                    continue
                    
                # Create Read object for non-header lines
                read = Read(line)
                
                # Only store primary mappings that are mapped
                if read.is_primary and read.is_mapped:
                    sam.reads.append(read)
                    
        return sam
    
    def reads_at_pos(self, seq_name: str, pos: int) -> list[Read]:
        """Return list of reads that map to given position"""
        return [read for read in self.reads 
                if read.rname == seq_name and read.base_at_pos(pos)]
    
    def pileup_at_pos(self, seq_name: str, pos: int) -> tuple[list[str], list[str]]:
        """Return tuple of lists containing base calls and quality scores at position"""
        bases = []
        quals = []
        
        for read in self.reads_at_pos(seq_name, pos):
            base = read.base_at_pos(pos)
            qual = read.qual_at_pos(pos)
            if base:
                bases.append(base)
                quals.append(qual)
                
        return bases, quals
    
    def consensus_at_pos(self, seq_name: str, pos: int) -> str:
        """Return majority base call at position, 'N' for any ties"""
        bases, _ = self.pileup_at_pos(seq_name, pos)
        if not bases:
            return ''
            
        # Count occurrences of each base/insertion
        base_counts = {}
        for base in bases:
            base_counts[base] = base_counts.get(base, 0) + 1
            
        if not base_counts:
            return 'N'
            
        # Get counts and total
        max_count = max(base_counts.values())
        total = len(bases)
        
        # Count how many bases have the max count
        bases_with_max = sum(1 for count in base_counts.values() if count == max_count)
        
        # Return 'N' if:
        # - Multiple bases have the same count (tie)
        # - No base has >50% representation
        if bases_with_max > 1 or max_count/total <= 0.5:
            return 'N'
            
        # Get the base with max count
        for base, count in base_counts.items():
            if count == max_count:
                return base
                
        return 'N'  # Fallback case
            
    
    def consensus(self, seq_name: str) -> str:
        """Return consensus sequence for given reference"""
        if seq_name not in self.references:
            return ''
            
        # Find range of positions covered by reads
        min_pos = float('inf')
        max_pos = 0
        for read in self.reads:
            if read.rname == seq_name:
                min_pos = min(min_pos, read.pos)
                max_pos = max(max_pos, read.pos + read.mapped_len)
                
        if min_pos == float('inf'):
            return ''
            
        # Build consensus sequence
        consensus_seq = []
        for pos in range(min_pos, max_pos):  
            base = self.consensus_at_pos(seq_name, pos)
            consensus_seq.append(base if base else 'N')
            
        return ''.join(consensus_seq)
    
    def best_consensus(self) -> str:
        """Return consensus sequence for reference with best mapping coverage"""
        # Count covered positions for each reference
        coverage = {}
        for ref in self.references:
            covered_positions = 0
            min_pos = float('inf')
            max_pos = 0
            
            # Find range of positions
            for read in self.reads:
                if read.rname == ref:
                    min_pos = min(min_pos, read.pos)
                    max_pos = max(max_pos, read.pos + read.mapped_len)
            
            if min_pos == float('inf'):
                continue
                
            # Count positions with >0 reads
            for pos in range(min_pos, max_pos + 1):
                if self.reads_at_pos(ref, pos):
                    covered_positions += 1
                    
            coverage[ref] = covered_positions
            
        if not coverage:
            return ''
            
        # Find reference with most positions covered
        best_ref = max(coverage.items(), key=lambda x: x[1])[0]
        return self.consensus(best_ref)