import random
import sys
import argparse

# Define constants for transition and emission matrices
TRANSITION_MATRIX = {
    'A': {'A': 0.999, 'B': 0.001},
    'B': {'A': 0.001, 'B': 0.999}
}

EMISSION_MATRIX = {
    'A': {
        'A': {'A': 0.25, 'C': 0.25, 'T': 0.25, 'G': 0.25},
        'C': {'A': 0.25, 'C': 0.25, 'T': 0.25, 'G': 0.25},
        'T': {'A': 0.25, 'C': 0.25, 'T': 0.25, 'G': 0.25},
        'G': {'A': 0.25, 'C': 0.25, 'T': 0.25, 'G': 0.25},
    },
    'B': {
        'A': {'A': 0.1, 'C': 0.1, 'T': 0.7, 'G': 0.1},
        'C': {'A': 0.4, 'C': 0.1, 'T': 0.4, 'G': 0.1},
        'T': {'A': 0.7, 'C': 0.1, 'T': 0.1, 'G': 0.1},
        'G': {'A': 0.4, 'C': 0.1, 'T': 0.4, 'G': 0.1}
    }
}


def random_seq(transition_matrix, emission_matrix, n):
    """
    Generate a synthetic DNA sequence and its corresponding hidden state sequence.

    Args:
        transition_matrix (dict): Transition probability matrix for hidden states.
        emission_matrix (dict): Emission probability matrix for observed nucleotides.
        n (int): Length of the generated sequence.

    Returns:
        list: A list containing the generated DNA sequence and its hidden state sequence.
    """
    state = random.choice(list(transition_matrix.keys()))
    seq = [random.choice(list(emission_matrix[state].keys()))]  # Initialize prev_n here
    hidden = [state]
    
    for i in range(n-1):
        prev_n = seq[i]
        nucleotides = emission_matrix[state][prev_n]
        keys = list(nucleotides.keys())   
        values = list(nucleotides.values())
        nuc_out = random.choices(keys, values)
        seq.extend(nuc_out)
        state = random.choices(
            list(transition_matrix[state].keys()),
            list(transition_matrix[state].values())
        )[0]
        hidden.extend(state)
    return [''.join(seq), ''.join(hidden)]

def main(args):
    """
    Main function to generate synthetic DNA sequences and stream them to stdout or save to a file.

    Args:
        args (argparse.Namespace): Command-line arguments.
    """
    length = args.length
    chroms = args.chroms

    if args.out_name:
        out_name = args.out_name
        outstream = open(out_name, "w")
    else:
        # If no output file is provided, stream to stdout
        outstream = sys.stdout

    outseq = []
    for _ in range(chroms):
        seq_oh = random_seq(TRANSITION_MATRIX, EMISSION_MATRIX, length)
        seq = seq_oh[0].lower()
        outseq.append(seq)

    with outstream as outfasta:
        for i, x in enumerate(outseq):
            outfasta.write(f">{i}\n{x}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("length", type=int, help="Desired length of the DNA sequence")
    parser.add_argument("chroms", type=int, help="Number of synthetic DNA sequences to generate")
    parser.add_argument("out_name", nargs='?', help="Name of the output file (optional)")
    args = parser.parse_args()
    main(args)
