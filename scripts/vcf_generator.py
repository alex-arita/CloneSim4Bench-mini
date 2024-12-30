#!/usr/bin/python3
#
# vcf_generator.py
# Last Edited: 2024/12/29
# Version: 1.0
#
# This script generates a general VCF (Variant Call Format) file and child VCFs
# with variants separated into specific VAF (Variant Allele Frequency) ranges.
# The resulting files are useful as benchmarks in evaluating somatic variant 
# calling performance.

import argparse
from datetime import datetime

def create_vcf_from_somatosim(somatosim_file: str, output_file: str) -> None:
    """
    Generates a VCF file from the specified SomatoSim output file, along with
    separate VCFs for variants within specific VAF ranges: <0.02, 0.02-0.05,
    0.05-0.1, and >0.1. Each VCF file is saved with a unique name indicating
    its respective VAF range.

    Parameters
    ----------
    somatosim_file : str
        Path to the input file generated by SomatoSim.
    output_file : str
        Path where the output VCF files will be saved.
    """

    # Define contig lines and INFO fields
    contig_lines = [
        "##contig=<ID=chr1,length=248956422>",
        "##contig=<ID=chr2,length=242193529>",
        "##contig=<ID=chr3,length=198295559>",
        "##contig=<ID=chr4,length=190214555>",
        "##contig=<ID=chr5,length=181538259>",
        "##contig=<ID=chr6,length=170805979>",
        "##contig=<ID=chr7,length=159345973>",
        "##contig=<ID=chr8,length=145138636>",
        "##contig=<ID=chr9,length=138394717>",
        "##contig=<ID=chr10,length=133797422>",
        "##contig=<ID=chr11,length=135086622>",
        "##contig=<ID=chr12,length=133275309>",
        "##contig=<ID=chr13,length=114364328>",
        "##contig=<ID=chr14,length=107043718>",
        "##contig=<ID=chr15,length=101991189>",
        "##contig=<ID=chr16,length=90338345>",
        "##contig=<ID=chr17,length=83257441>",
        "##contig=<ID=chr18,length=80373285>",
        "##contig=<ID=chr19,length=58617616>",
        "##contig=<ID=chr20,length=64444167>",
        "##contig=<ID=chr21,length=46709983>",
        "##contig=<ID=chr22,length=50818468>",
        "##contig=<ID=chrX,length=156040895>",
        "##contig=<ID=chrY,length=57227415>",
        "##contig=<ID=chrM,length=16569>",
        '##INFO=<ID=iAF,Number=1,Type=Float,Description="Input allele frequency">',
        '##INFO=<ID=iDP,Number=1,Type=Integer,Description="Input depth">',
        '##INFO=<ID=AF,Number=1,Type=Float,Description="Output allele frequency">',
        '##INFO=<ID=DP,Number=1,Type=Integer,Description="Output depth">'
    ]

    # Get current date
    date = datetime.now()

    # Define output files for each VAF range
    vaf_ranges = {
        "all": open(f"{output_file}_all.vcf", 'w'),
        "0_to_002": open(f"{output_file}_AF_0_to_002.vcf", 'w'),
        "002_to_005": open(f"{output_file}_AF_002_to_005.vcf", 'w'),
        "005_to_01": open(f"{output_file}_AF_005_to_01.vcf", 'w'),
        "01_to_1.vcf": open(f"{output_file}_AF_01_to_1.vcf", 'w')
    }

    # Write VCF headers
    for vcf_file in vaf_ranges.values():
        vcf_file.write("##fileformat=VCFv4.2\n")
        vcf_file.write(f"##fileDate={date.year}{date.month:02}{date.day:02}\n")
        vcf_file.write("##source=SomatoSim\n")
        for line in contig_lines:
            vcf_file.write(f"{line}\n")
        vcf_file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

    # Process the input SomatoSim file
    with open(somatosim_file, 'r') as infile:
        infile.readline()  # Skip header line

        for line in infile:
            fields = line.strip().split()
            chrom, pos = fields[0], fields[2]
            ref, alt = fields[7], fields[8]
            input_VAF, input_cov = float(fields[3]), fields[4]
            output_VAF, output_cov = fields[5], fields[6]

            # Create INFO field
            info = f"iAF={input_VAF};iDP={input_cov};AF={output_VAF};DP={output_cov}"
            vcf_line = f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t.\tPASS\t{info}\n"

            # Write to the general file
            vaf_ranges["all"].write(vcf_line)

            # Write to specific VAF range files
            if input_VAF < 0.02:
                vaf_ranges["0_to_002"].write(vcf_line)
            elif 0.02 <= input_VAF < 0.05:
                vaf_ranges["002_to_005"].write(vcf_line)
            elif 0.05 <= input_VAF < 0.1:
                vaf_ranges["005_to_01"].write(vcf_line)
            elif input_VAF >= 0.1:
                vaf_ranges["01_to_1.vcf"].write(vcf_line)

    # Close all files
    for vcf_file in vaf_ranges.values():
        vcf_file.close()

def main():
    """
    Parses command-line arguments and initiates the VCF creation process.
    """
    parser = argparse.ArgumentParser(description = \
        'Generate a VCF and VAF-specific VCF files from SomatoSim output')
    parser.add_argument('-i', '--input', dest='input', required=True,
                        type=str, help='Input SomatoSim file')
    parser.add_argument('-o', '--output', dest='output', required=True,
                        type=str, help='Base name for output VCF files')
    args = parser.parse_args()

    create_vcf_from_somatosim(args.input, args.output)

if __name__ == "__main__":
    main()