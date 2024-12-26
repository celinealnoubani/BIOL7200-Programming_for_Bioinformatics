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
		self.is_mapped: bool = not bool(self.flag & 4) # 4 bit not in flag
		self.is_forward: bool = not bool(self.flag & 16)
		self.is_reverse: bool = bool(self.flag & 16)
		self.is_primary: bool = not (bool(self.flag & 256) or bool(self.flag & 2048)) # not secondary or supplemental

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

		idx = 0 # track where we are in read seq
		bases = [] # list to build up over time without costly string concatenation
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
