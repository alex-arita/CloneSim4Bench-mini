#!/usr/bin/python3
#
# matrix_gen.py
# v1.3
# Last edit 2024/11/18
#
# Processes both general and detailed comparisons done by vcf-compare
# to generate matrices that R could process easily.

import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def metrics(FILE: str, CALLER: str, TP: int, TN: int, FP: int, FN: int) -> list:
    """
    Calculate various metrics based on True Positives, True Negatives,
    False Positives, and False Negatives.
    """
    sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0.0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0.0
    fpr = FP / (FP + TN) if (FP + TN) > 0 else 0.0
    fnr = FN / (TP + FN) if (TP + FN) > 0 else 0.0
    f1_score = (2 * precision * sensitivity) / (precision + sensitivity) \
                if (precision + sensitivity) > 0 else 0.0

    return [FILE, CALLER, TP, TN, FP, FN, sensitivity, specificity, precision,
            accuracy, fpr, fnr, f1_score]

def general_matrix(input_file: str, output_file: str) -> None:
    """
    Generate a general matrix from the input VCF file and save it to an
    output file.
    """
    vcs = ["FreeBayes", "LoFreq", "Mutect2", "Strelka2", "VarScan2"]
    matrix = [["File", "Caller", "TP", "TN", "FP", "FN", "Sensitivity",
               "Specificity", "Precision", "Accuracy", "FPR", "FNR", "F1 Score"]]

    try:
        with open(input_file) as input, open(output_file, 'w') as output:
            TP = TN = FP = FN = 0
            FILE = ""
            CALLER = ""

            for line in input:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("FL"):
                    if FILE:
                        matrix.append(metrics(FILE, CALLER, TP, TN, FP, FN))
                    attr = line.split()
                    FILE = attr[1]
                    CALLER = ""
                    TN = int(attr[2])
                    TP = FP = FN = 0

                elif any(vc in line for vc in vcs):
                    attr = line.split()
                    if CALLER != attr[0]:
                        if CALLER:
                            matrix.append(metrics(FILE, CALLER, TP, TN, FP, FN))
                        CALLER = attr[0]
                        TP = FP = FN = 0

                    if len(attr) > 4:
                        TP = int(attr[1])
                    elif attr[2].endswith("_all.vcf.gz"):
                        FN = int(attr[1])
                    else:
                        FP = int(attr[1])

            if FILE and CALLER:
                matrix.append(metrics(FILE, CALLER, TP, TN, FP, FN))

            for row in matrix:
                output.write("\t".join(map(str, row)) + "\n")

    except Exception as e:
        logging.error(f"Error while processing general_matrix: {e}")

def detailed_matrix(input_file: str, output_file: str) -> None:
    """
    Generate a detailed matrix from the input VCF file and save it to an output file.
    """
    AF_RANGES = ["< 0.02", "0.02 - 0.05", "0.05 - 0.1", "> 0.1"]
    matrix = [["File", "Caller", "AF", "total_variants", "total_called", "Ratio"]]

    current_file = ""
    current_caller = ""
    current_af_index = -1
    total_variants = 0
    called_variants = 0

    try:
        with open(input_file, 'r') as input, open(output_file, 'w') as output:
            for line in input:

                if line.startswith("FL"):
                    current_file = line.split()[1]
                    current_caller = ""
                    current_af_index = 0
                    total_variants = 0
                    called_variants = 0

                elif "_AF_0_to_002" == line.strip():
                    current_af_index = 0

                elif "_AF_002_to_005" == line.strip():
                    current_af_index = 1

                elif "_AF_005_to_01" == line.strip():
                    current_af_index = 2

                elif "_AF_01_to_1" == line.strip():
                    current_af_index = 3

                elif line == "\n":
                    if current_file:
                        matrix.append([
                            current_file,
                            current_caller,
                            AF_RANGES[current_af_index],
                            total_variants,
                            called_variants,
                            round((called_variants / total_variants), 2) \
                            if total_variants > 0 else 0
                        ])
                    total_variants = 0
                    called_variants = 0

                else:
                    fields = line.split()
                    current_caller = fields[0]
                    if len(fields) > 4:
                        called_variants += int(fields[1])
                        total_variants += int(fields[1])
                    elif "x_AF_" in line:
                        total_variants += int(fields[1])

            for row in matrix:
               output.write("\t".join(map(str, row)) + "\n")

    except Exception as e:
        logging.error(f"Error while processing detailed_matrix: {e}")

def main():
    parser = argparse.ArgumentParser(description='matrix_gen')
    parser.add_argument('-g', '--general_results', dest='general',
                        required=True, type=str)
    parser.add_argument('-d', '--detailed_results', dest='detailed',
                        required=True, type=str)
    args = parser.parse_args()

    general_input = args.general
    general_output = general_input.rsplit('.', 1)[0] + ".tsv"
    detailed_input = args.detailed
    detailed_output = detailed_input.rsplit('.', 1)[0] + ".tsv"

    general_matrix(general_input, general_output)
    detailed_matrix(detailed_input, detailed_output)

if __name__ == "__main__":
    main()