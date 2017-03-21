#!/usr/bin/env python

def complement(bases):
  complement_str = ''
  c_base = dict(A='T', T='A', C='G', G='C')
  for base in bases:
    base = base.upper()
    complement_str += c_base.get(base, base)

  return complement_str

def add_decoration(thestring, decoration):
    return decoration + thestring + decoration

def product_of_cubes(n):
    total = 1
    for num in range(1, n+1):
        total *= num ** 3
    return total

def remove_adapter(dnalist, adapter):
    trimmed_seqs = []
    adapter_length = len(adapter)
    for seq in dnalist:
        if seq.startswith(adapter):
            seq = seq[adapter_length:]
        trimmed_seqs.append(seq)
    return trimmed_seqs

def piece_lengths(dnastring):
    enzyme = 'GAATTC'
    if enzyme in dnastring:
        position = dnastring.find(enzyme)
        piece1 = len(dnastring[:position+1])
        piece2 = len(dnastring[position+1:])
        return [piece1, piece2]
    else:
        return []

def motif_count(dnastring, motif):
    return dnastring.upper().count(motif.upper())

if __name__ == '__main__':
    print(product_of_cubes(10))
