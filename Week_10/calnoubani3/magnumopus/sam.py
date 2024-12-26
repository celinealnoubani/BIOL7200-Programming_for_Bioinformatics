#!/usr/bin/env python3

import re

class Read:
    def __init__(self, line):
        fields = line.strip().split()  # split by whitespace

        # Assigning each field to its attribute
        self.qname = fields[0]  # query name
        self.flag = int(fields[1])  #flag
        self.rname = fields[2]  # reference name
        self.pos = int(fields[3])  # 1-based leftmost mapping position
        self.mapq = int(fields[4])  # mapping quality
        self.cigar = fields[5]  # cigar string
        self.rnext = fields[6]  # reference name of next read
        self.pnext = int(fields[7])  # position of next read
        self.tlen = int(fields[8])  # observed template length
        self.seq = fields[9]  # segment sequence
        self.qual = fields[10]  # ASCII of phred-scaled base quality

    # Check if read is mapped
    @property
    def is_mapped(self):
        return not (self.flag & 0x4)

    # Check if read is mapped in forward direction
    @property
    def is_forward(self):
        return not (self.flag & 0x10)

    # Check if read is mapped in reverse direction
    @property
    def is_reverse(self):
        return bool(self.flag & 0x10)

    # Check if read is the primary alignment
    @property
    def is_primary(self):
        return not (self.flag & 0x100) and not (self.flag & 0x800)

    # Get the base at a specific position in the reference
    def base_at_pos(self, pos: int) -> str:
        # Parse the cigar string using regex to extract operations & their lengths
        cigar_pattern = re.findall(r'(\d+)([MIDNSHP=X])', self.cigar)
        current_ref_pos = self.pos
        current_read_pos = 0

        # Iterate over cigar operations
        for length, op in cigar_pattern:
            length = int(length)

            if op == 'M':  # Match or mismatch
                if current_ref_pos <= pos < current_ref_pos + length:
                    return self.seq[current_read_pos + (pos - current_ref_pos)]
                current_ref_pos += length
                current_read_pos += length

            elif op == 'D':  # Deletion in reference
                if current_ref_pos <= pos < current_ref_pos + length:
                    return '' 
                current_ref_pos += length

            elif op == 'I':  # Insertion in read
                current_read_pos += length

            elif op == 'S':  # Soft clipping (not part of alignment)
                current_read_pos += length 

        # If the position is not covered by the alignment
        return ''

    # Get the quality score at a specific position in the reference
    def qual_at_pos(self, pos: int) -> str:
        cigar_pattern = re.findall(r'(\d+)([MIDNSHP=X])', self.cigar)
        current_ref_pos = self.pos
        current_read_pos = 0

        for length, op in cigar_pattern:
            length = int(length)

            if op == 'M':  # Match or mismatch
                if current_ref_pos <= pos < current_ref_pos + length:
                    return self.qual[current_read_pos + (pos - current_ref_pos)]
                current_ref_pos += length
                current_read_pos += length

            elif op == 'D':  # Deletion in reference
                current_ref_pos += length

            elif op == 'I':  # Insertion in read
                current_read_pos += length

            elif op == 'S':  # Soft clipping (not part of alignment)
                current_read_pos += length

        return ''

    # Get mapped portion of the sequence
    def mapped_seq(self) -> str:
        cigar_pattern = re.findall(r'(\d+)([MIDNSHP=X])', self.cigar)
        mapped_sequence = []
        current_read_pos = 0

        for length, op in cigar_pattern:
            length = int(length)

            if op == 'M':  # Match or mismatch
                mapped_sequence.append(self.seq[current_read_pos:current_read_pos + length])
                current_read_pos += length

            elif op == 'D':  # Deletion in reference
                mapped_sequence.append('-' * length)

            elif op == 'I':  # Insertion in read
                # Insertions are included in the mapped portion
                mapped_sequence.append(self.seq[current_read_pos:current_read_pos + length])
                current_read_pos += length

            elif op == 'S':  # Soft clipping (not part of alignment)
                current_read_pos += length

        return ''.join(mapped_sequence)

# Testing
if __name__ == "__main__":
    line = "ERR11767307.541398\t163\tFusibacter_paucivorans\t1\t60\t68S83M\t=\t314\t464\tCAAGAAACAAACCATAAAGCCAGATATTTTGATAACAATAGTATCTGAGCCTGATAAACTTTTATTTGAGAGTTTGATCCTGGCTCAGGATGAACGCTGGCG\tFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    
    read = Read(line)
    print(f"QNAME: {read.qname}")
    print(f"FLAG: {read.flag}")
    print(f"CIGAR: {read.cigar}")
    print(f"Is Mapped: {read.is_mapped}")
    print(f"Is Forward: {read.is_forward}")
    print(f"Is Reverse: {read.is_reverse}")
    print(f"Is Primary: {read.is_primary}")
    # Testing base_at_pos 
    print(f"Base at position 5: {read.base_at_pos(5)}")  # example test
    print(f"Base at position 100: {read.base_at_pos(100)}")  # example test
    # Testing qual_at_pos 
    print(f"Quality at position 5: {read.qual_at_pos(5)}")
    print(f"Quality at position 100: {read.qual_at_pos(100)}")
    # Testing mapped_seq 
    print(f"Mapped Sequence: {read.mapped_seq()}")