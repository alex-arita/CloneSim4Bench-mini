#!/usr/bin/bash
# create_directories.sh
#
# Last Edit: 2024/12/29
# By: Alex Fernando Arita
# Version 1.0
#
# Sets the directories for the entire project.

show_help() {
    echo "Usage: $0 <project_dir>"
    echo "Example:"
    echo "  bash $0 /path/for/project"
    exit 0
}

PROJECT_DIR="$1"

# Check for required arguments
if [ -z "$PROJECT_DIR" ]; then
    echo "Error: No directory provided."
    echo "Usage: $0 -i <project_dir>"
    exit 1
fi

# Set output directory
OUTPUT_DIR=$(realpath "$1")
echo "Creating Proyect folders..."

# Ensure write permissions
if [ ! -w "$(dirname "$OUTPUT_DIR")" ]; then
    echo "Error: No write permission in the parent directory of $OUTPUT_DIR"
    exit 1
fi

# Create Common Directories
mkdir -p "$OUTPUT_DIR" || { echo "Failed to create $OUTPUT_DIR"; exit 1; }
mkdir -p "$OUTPUT_DIR"/Analysis
mkdir -p "$OUTPUT_DIR"/BAMs
mkdir -p "$OUTPUT_DIR"/Logs
mkdir -p "$OUTPUT_DIR"/Metrics
mkdir -p "$OUTPUT_DIR"/Reference
mkdir -p "$OUTPUT_DIR"/tmp

# Create Directories for Stochastic Simulation
mkdir -p "$OUTPUT_DIR"/BAMs_mutated/Stochastic
mkdir -p "$OUTPUT_DIR"/BEDs/Stochastic
mkdir -p "$OUTPUT_DIR"/VCFs/Stochastic/REFs
mkdir -p "$OUTPUT_DIR"/VCFs/Stochastic/FreeBayes
mkdir -p "$OUTPUT_DIR"/VCFs/Stochastic/LoFreq
mkdir -p "$OUTPUT_DIR"/VCFs/Stochastic/Mutect2/tmp
mkdir -p "$OUTPUT_DIR"/VCFs/Stochastic/Strelka2
mkdir -p "$OUTPUT_DIR"/VCFs/Stochastic/VarScan2

# Create Directories for Guided Simulation
mkdir -p "$OUTPUT_DIR"/BAMs_mutated/Guided
mkdir -p "$OUTPUT_DIR"/BEDs/Guided
mkdir -p "$OUTPUT_DIR"/VCFs/Guided/REFs
mkdir -p "$OUTPUT_DIR"/VCFs/Guided/FreeBayes
mkdir -p "$OUTPUT_DIR"/VCFs/Guided/LoFreq
mkdir -p "$OUTPUT_DIR"/VCFs/Guided/Mutect2/tmp
mkdir -p "$OUTPUT_DIR"/VCFs/Guided/Strelka2
mkdir -p "$OUTPUT_DIR"/VCFs/Guided/VarScan2