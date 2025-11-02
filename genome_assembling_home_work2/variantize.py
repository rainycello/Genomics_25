import random
import numpy as np
import math
import os
import sys

# Define the DNA sequence modification functions directly in the main script

def snps(seq, prob=0.001):
    """
    Introduce single nucleotide polymorphisms (SNPs) into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing an SNP at each position.

    Returns:
        str: DNA sequence with SNPs.
    """
    outseq = ""
    for i in seq:
        r = random.uniform(0, 1)
        if r <= prob:
            outseq += random.choice(["A", "C", "T", "G"])
        else:
            outseq += i
    return outseq

def small_indels(seq, prob=0.0001):
    """
    Introduce small insertions and deletions (indels) into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing a small indel at each position.

    Returns:
        str: DNA sequence with small indels.
    """
    rng = np.random.default_rng()
    outseq = ""
    i = 0
    while i < len(seq):
        nuc = seq[i]
        r = random.uniform(0, 1)
        if r <= prob:
            v_type = random.choice(["i", "d"])
            size = int(np.ceil(rng.gamma(0.5, 50)))
            if v_type == "i":
                outseq += nuc
                for n in range(0, size):
                    outseq += random.choice(["A", "C", "T", "G"])
            else:
                for n in range(0, size):
                    i += 1
        else:
            outseq += nuc
        i += 1
    return outseq

def large_indels(seq, prob=0.0001):
    """
    Introduce large insertions and deletions (indels) into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing a large indel at each position.

    Returns:
        str: DNA sequence with large indels.
    """
    rng = np.random.default_rng()
    outseq = ""
    i = 0
    while i < len(seq):
        nuc = seq[i]
        r = random.uniform(0, 1)
        if r <= prob:
            v_type = random.choice(["i", "d"])
            size = int(np.ceil(rng.gamma(2, 300)))
            if v_type == "i":
                outseq += nuc
                for n in range(0, size):
                    outseq += random.choice(["A", "C", "T", "G"])
            else:
                for n in range(0, size):
                    i += 1
        else:
            outseq += nuc
        i += 1
    return outseq

def complement(seq):
    """
    Generate the complement of a DNA sequence.

    Args:
        seq (str): Input DNA sequence.

    Returns:
        str: Complement of the input sequence.
    """
    outseq = ""
    dic = {"A": "T", "T": "A", "C": "G", "G": "C"}
    for i in seq:
        outseq += dic[i]
    return outseq

def inv(seq, prob=0.0001):
    """
    Introduce inversions into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing an inversion.

    Returns:
        str: DNA sequence with inversions.
    """
    rng = np.random.default_rng()
    outseq = ""
    i = 0
    while i < len(seq):
        nuc = seq[i]
        r = random.uniform(0, 1)
        if r <= prob:
            size = int(np.ceil(rng.gamma(2, 300)))
            outseq += complement(seq[i:i + size][::-1].upper())
            i += size
        else:
            outseq += nuc
            i += 1
    return outseq

def tan_dup(seq, prob=0.0001):
    """
    Introduce tandem duplications into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing a tandem duplication.

    Returns:
        str: DNA sequence with tandem duplications.
    """
    rng = np.random.default_rng()
    outseq = ""
    i = 0
    n_dup = rng.poisson(8) + 1
    while i < len(seq):
        nuc = seq[i]
        r = random.uniform(0, 1)
        if r <= prob:
            size = int(np.ceil(rng.gamma(0.3, 1000)))
            outseq += seq[i:i + size].upper()
            for n in range(n_dup):
                outseq += seq[i:i + size].upper()
            i += size
        else:
            outseq += nuc
            i += 1
    return outseq

def disp_dup(seq, prob=0.00001):
    """
    Introduce dispersed duplications into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing a dispersed duplication.

    Returns:
        str: DNA sequence with dispersed duplications.
    """
    rng = np.random.default_rng()
    i = 0
    events = math.floor(len(seq) * prob)
    for event in range(events):
        outseq = ""
        seed = int(random.uniform(0, len(seq)))
        target = int(random.uniform(0, len(seq)))
        size = int(np.ceil(rng.gamma(3, 200)))
        outseq += seq[:target]
        outseq += seq[seed: seed + size].upper()
        outseq += seq[target:]
        seq = outseq
    return outseq

def nr_trans(seq, prob=0.00001):
    """
    Introduce non-reciprocal translocations into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing a non-reciprocal translocation.

    Returns:
        str: DNA sequence with non-reciprocal translocations.
    """
    rng = np.random.default_rng()
    i = 0
    events = math.floor(len(seq) * prob)
    if events == 0:
        return seq
    for event in range(events):
        outseq = ""
        size = int(np.ceil(rng.gamma(3, 1000)))
        seed = int(random.uniform(0, len(seq)))
        target = int(random.uniform(0, len(seq)))
        if size > abs(seed - target):
            size = abs(seed - target)
        if size > len(seq) - seed:
            size = len(seq) - seed
        if target < seed:
            outseq += seq[:target]
            outseq += seq[seed: seed + size].upper()
            outseq += seq[target:seed]
            outseq += seq[seed + size:]
        elif seed < target:
            outseq += seq[:seed]
            outseq += seq[seed + size:target]
            outseq += seq[seed: seed + size].upper()
            outseq += seq[target:]
        else:
            outseq = seq
        seq = outseq
    return outseq

def r_trans(seq, prob=0.00001):
    """
    Introduce reciprocal translocations into a DNA sequence.

    Args:
        seq (str): Input DNA sequence.
        prob (float): Probability of introducing a reciprocal translocation.

    Returns:
        str: DNA sequence with reciprocal translocations.
    """
    rng = np.random.default_rng()
    i = 0
    events = math.floor(len(seq) * prob)
    if events == 0:
        return seq
    for event in range(events):
        outseq = ""
        seed = int(random.uniform(0, len(seq)))
        target = int(random.uniform(0, len(seq)))
        s_size = int(np.ceil(rng.gamma(3, 1000)))
        t_size = int(np.ceil(rng.gamma(3, 1000)))
        if target < seed:
            outseq += seq[:target]
            outseq += seq[seed: seed + s_size].upper()
            outseq += seq[target + t_size:seed]
            outseq += seq[target:target + t_size].upper()
            outseq += seq[seed + s_size:]
        elif seed < target:
            outseq += seq[:seed]
            outseq += seq[target:target + t_size].upper()
            outseq += seq[seed + s_size:target]
            outseq += seq[seed: seed + s_size].upper()
            outseq += seq[target + t_size:]
        else:
            outseq = seq
        seq = outseq
    return outseq

# Main function
def main():
    in_fasta = sys.argv[1]  # Input FASTA file containing DNA sequences
    opts = sys.argv[2]  # Options for sequence modification

    fadict = {}  # Initialize a dictionary to store sequences

    # Read the input FASTA file and store sequences in 'fadict'
    with open(in_fasta) as plik:
        idx = ""
        for line in plik:
            if line.startswith(">"):
                fadict[line.strip()] = ""
                idx = line.strip()
            else:
                fadict[idx] += line.strip()

    # Iterate through the sequences in 'fadict' and apply selected modifications
    for key in fadict:
        seq = fadict[key].lower()  # Convert the sequence to lowercase
        for opt in opts:
            if opt == "s":
                seq = snps(seq)  # Introduce SNPs
            elif opt == "i":
                seq = small_indels(seq)  # Introduce small indels
            elif opt == "l" or opt == "I":
                seq = large_indels(seq)  # Introduce large indels
            elif opt == "v":
                seq = inv(seq)  # Introduce inversions
            elif opt == "t":
                seq = tan_dup(seq)  # Introduce tandem duplications
            elif opt == "d":
                seq = disp_dup(seq)  # Introduce dispersed duplications
            elif opt == "n":
                seq = nr_trans(seq)  # Introduce non-reciprocal translocations
            elif opt == "r":
                seq = r_trans(seq)  # Introduce reciprocal translocations
            else:
                print("WRONG OPTION")  # Print an error message for unknown options


        # Print the modified sequence with its key (header) to standard output
        print(f"{key}\n{seq.upper()}\n")

if __name__ == "__main__":
    main()  
