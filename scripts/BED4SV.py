#!/usr/bin/python3
#
# BED4SV.py
# v1.4 (adapted for Python 3.6)
# Last edit 2024/11/30
#
# It processes a COSMIC VCF or capture probes BED file, generating a modified
# BED for use with SomatoSim to simulate somatic mutations.
# Fixes the RAM usage for big files.

import argparse
import random
import gzip
import sys
from typing import IO, List, TextIO

def open_file(input: str) -> IO:
    """
    Handles the opening of files, either uncompressed or compressed (.gz).

    Parameters
    ----------
    input:
        Filepath to the BED or VCF file.

    Returns
    -------
    IO:
        File opened.
    """
    if input.endswith('.gz'):
        return gzip.open(input, 'rt')
    else:
        return open(input, 'rt')

import gzip

def n_lines_in_file(input: str) -> int:
    """
    Count the number of non-header lines using block reading for large files.
    """
    lineas = 0
    tamano_bloque = 4096 * 4096  # Block size
    open_func = gzip.open if input.endswith('.gz') else open

    with open_func(input, 'rb') as archivo:
        while True:
            bloque = archivo.read(tamano_bloque)
            if not bloque:
                break
            lines = bloque.split(b'\n')  # Split block into lines
            lineas += sum(1 for line in lines if not line.startswith(b"##"))
    return lineas


def is_valid(contig_name: str) -> bool:
    """
    Determines if a given contig name is classified as an alternative.

    Parameters
    ----------
    contig_name : str
        The contig name from either a BED or VCF file (typically the
        first field).

    Returns
    -------
    bool
        True if valid, False otherwise
    """
    return not any(keyword in contig_name for keyword in \
        ['alt', 'random', 'Un', 'chrUn', 'hap', 'gl', 'ki', 'fix'])

def random_lines_selector(input: TextIO, n_lines_in_file: int,
                            n_lines_required: int) -> List[str]:
    """
    Picks random reads from a file without loading the whole file into memory.

    Parameters
    ----------
    input: TextIO
        File object for the lines in the VCF or BED file from which lines
        are going to be picked.

    n_lines_in_file: int
        Number of lines in the entire file.

    n_lines_required: int
        Number of lines to be picked.

    Returns
    -------
    List[str]:
        List of lines containing random picked lines from the VCF or BED file.
    """
    selected = set()
    while len(selected) < n_lines_required:
        position = random.randint(0, n_lines_in_file - 1)
        input.seek(position)
        input.readline()
        line = input.readline()
        attr = line.strip().split()
        if len(attr) > 4 and not line.startswith("#") and \
            is_valid(attr[0]) and len(attr[4]) == 1:
            selected.add(line.strip())
    return selected

def guided(input_file: str, output: str, vaf_low: float, vaf_high: float,
           number: int, seed: int) -> int:
    """
    Generates a modified BED file using a COSMIC VCF as a guide for simulation.

    Parameters
    ----------
    input_file : str
        Path to the VCF or GNU zip (GZ) VCF file containing well-known mutations
        from COSMIC.

    output : str
        Filepath for the output BED file.

    vaf_low : float
        The lowest allele frequency to use for the simulation (VAF lower bound).

    vaf_high : float
        The highest allele frequency to use for the simulation (VAF upper
        bound).

    number : int
        Number of variants to include in the output BED file.

    seed : int
        Seed for the random number generator to allow reproducibility of
        results.

    Returns
    -------
    int
        Returns 0 on successful execution, or 1 if an error occurs.
    """
    total_lines = n_lines_in_file(input_file)
    try:
        if seed:
            random.seed(seed)

        VCF_in = open_file(input_file)
        BED_out = open(output + '.bed', 'w')

        selection = random_lines_selector(VCF_in, total_lines, number)

        if vaf_low is not None and vaf_high is not None:
            for i, line in enumerate(selection, 1):
                fields = line.strip().split('\t')
                vaf = round(random.uniform(vaf_low, vaf_high), 3)
                BED_out.write(
                    f'chr{fields[0]}\t{int(fields[1])-1}\t{int(fields[1])}\t{vaf}\t{fields[4]}'
                )
                if i < number:
                    BED_out.write('\n')

        VCF_in.close()
        BED_out.close()
        return 0

    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}", file=sys.stderr)
        return 1

def stochastic(input: str, output: str, vaf_low: float, vaf_high: float, 
               number: int, seed: int) -> int:
    """
    Generates a modified BED file stochastically using a capture BED file.

    Parameters
    ----------
    input : str
        Path to the BED file (or gzipped BED file) containing capture regions.

    output : str
        Filepath for the output BED file.

    vaf_low : float
        The lowest allele frequency to use for the simulation
        (VAF lower bound).

    vaf_high : float
        The highest allele frequency to use for the simulation
        (VAF upper bound).

    number : int
        Number of variants to include in the output BED file.

    seed : int
        Seed for the random number generator to allow reproducibility of
        results.

    Returns
    -------
    int
        Returns 0 on successful execution, or 1 if an error occurs.
    """
    try:
        if seed:
            random.seed(seed)

        try:
            BED_in = open_file(input)
            BED_out = open(output + '.bed', 'w')
        except Exception as e:
            print(f"ERROR: Failed to open input or output files: {e}",
                    file=sys.stderr)
            return 1

        try:
            filtered_lines = [line for line in BED_in if \
                                is_valid(line.split()[0])]
        except Exception as e:
            print(f"ERROR: Failed to process the input BED file: {e}",
                    file=sys.stderr)
            BED_in.close()
            BED_out.close()
            return 1

        if len(filtered_lines) < number:
            print(
            "ERROR: Not enough regions available for the requested selection.",
            file=sys.stderr
                )
            BED_in.close()
            BED_out.close()
            return 1

        try:
            selection = random.choices(filtered_lines, k=number)
        except Exception as e:
            print(f"ERROR: Failed during random selection: {e}",
                  file=sys.stderr)
            BED_in.close()
            BED_out.close()
            return 1

        try:
            for i, line in enumerate(selection, 1):
                attr = line.strip().split()
                x = random.choice(range(int(attr[1]), int(attr[2]) + 1))

                if vaf_low is not None and vaf_high is not None:
                    vaf = round(random.uniform(vaf_low, vaf_high), 3)
                    BED_out.write(f'{attr[0]}\t{x}\t{x+1}\t{vaf}')
                else:
                    BED_out.write(f'{attr[0]}\t{x}\t{x+1}')

                if i < number:
                    BED_out.write('\n')
        except Exception as e:
            print(f"ERROR: Failed during writing output: {e}", file=sys.stderr)
            BED_in.close()
            BED_out.close()
            return 1

        BED_in.close()
        BED_out.close()
        return 0

    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}", file=sys.stderr)
        return 1

def main() -> None:
    parser = argparse.ArgumentParser(description='BED generator')
    parser.add_argument('-i', '--input', dest='input',
                        required=True, type=str, default=None)
    parser.add_argument('-o', '--output', dest='output',
                        required=True, type=str)
    parser.add_argument('-n', '--variants-number', dest='number',
                        required=True, type=int)
    parser.add_argument('-s', '--seed', dest='seed',
                        required=False, type=int)
    parser.add_argument('--vaf-low', dest='vaf_low',
                        required=False, type=float)
    parser.add_argument('--vaf-high', dest='vaf_high',
                        required=False, type=float)
    args = parser.parse_args()

    print("                            BED4SV                            \n" \
          "--------------------------------------------------------------")

    method = 0
    if args.input.endswith(".bed") or args.input.endswith(".bed.gz"):
        method = 1

    vaf_low = args.vaf_low
    vaf_high = args.vaf_high
    seed = args.seed
    number = args.number
    output = args.output

    print(f"\nInput File: {args.input}\nNumber of Mutations to be selected: {number}\n"
          f"Lowest VAF: {vaf_low}\nHighest VAF: {vaf_high}\n")

    if method == 0:
        guided(args.input, output, vaf_low, vaf_high, number, seed)
    else:
        stochastic(args.input, output, vaf_low, vaf_high, number, seed)

if __name__ == "__main__":
    main()