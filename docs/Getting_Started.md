# Getting Started

## Index

-   [Conda](#conda)
    -   [Installation](#installation)
    -   [Environments](#environments)
-   [Somatic Variants Simulation](#somatic-variants-simulation)
    -   [SomatoSim](#somatosim)
    -   [External files](#external-files)
        -   [Cosmic](#cosmic)
        -   [Exome Probeset](#exome-probeset)
-   [Variant Caller](#variant-callers)
    -   [FreeBayes](#freebayes)
    -   [LoFreq](#lofreq)
    -   [GATK Mutect2](#gatk-mutect2)
    -   [Strelka2](#strelka2)
    -   [VarScan2](#varscan2)
-   [Variants Comparison](#variants-comparison)
    -   [BCFTools](#bcftools)
    -   [VCFTools](#vcftools)

## Conda

### Installation

Anaconda is a requirement for a great number of processes to be performed. To install it, and depending on the system you are working with, a well-documented guide is available in the [Anaconda Documentation](https://docs.anaconda.com/anaconda/install/).

### Environments

Conda environments can be set up using the .yml file located in the corresponding folder. To create an environment, use the following command:

```bash
conda env create -f <environment_name>.yml
```

This will install all the dependencies and configurations specified in the .yml file.

## Somatic Variants Simulation

### SomatoSim

SomatoSim can be cloned from GitHub, where a list of dependencies is provided. To do this, run the following commands:

```bash
git clone https://github.com/BieseckerLab/SomatoSim.git
cd SomatoSim
python3 -m pip install .
```

It is important to note that a common issue mentioned in the repository is related to the decimal delimiter. To address this, the authors provide a Docker image available at Docker Hub. Additionally, a Singularity image can be generated using the following commands:

```bash
module load singularity
singularity pull docker://marwanhawari/somatosim
```

**Note**: 
-   The SomatoSim image must be located in the tools folder. Otherwise, it will be downloaded by the script.
-   Due to the issue with the decimal delimiter, SomatoSim was configured to work from a SIF image.
-   For further information about the software and its parameters, [click here](SomatoSim.md).

### External files

BED42SV is designed to work with either the COSMIC GenomeScreensMutant VCF (for guided mode) or an Exome Capture Probeset BED (for stochastic mode). Neither of these files is provided with this framework; obtaining or replacing them is the responsibility of the user. However, a step-by-step guide is provided below.

Please note that switching between stochastic and guided modes requires the user to modify the script and update the file path to the appropriate file for the selected mode.

#### COSMIC

The Catalogue Of Somatic Mutations In Cancer (COSMIC) is a public resource maintained by the Wellcome Sanger Institute. The data is available for free, although registration may be required to obtain the GenomeScreensMutant VCF.

### Exome probeset

The exome probesets are available for free at the [University of California Santa Cruz's Genome Browser](https://genome.ucsc.edu/cgi-bin/hgTables). Attention must be pay since both probe regions and targeted regions are available.

## Variant Callers

As previously mentioned, CloneSim4Bench integrates five variant callers for somatic variant detection: [FreeBayes](https://github.com/freebayes/freebayes), [LoFreq](https://github.com/CSB5/lofreq), [GATK Mutect2](https://github.com/broadinstitute/gatk),  [Strelka2](https://github.com/Illumina/strelka), [VarScan2](https://github.com/dkoboldt/varscan). The table below provides a concise summary of their algorithms and probabilistic models.

| Variant Caller | Algorithm Type    | Probabilistic Model                              | Designed For                 | Key Features                                                                                   |
|----------------|-------------------|-------------------------------------------------|------------------------------|------------------------------------------------------------------------------------------------|
| FreeBayes      | Bayesian          | Bayesian                                        | Germline and somatic variants| Uses local haplotype-based calling; can detect complex variants (MNVs, large indels).          |
| LoFreq         | Probabilistic     | Maximum likelihood model                        | Somatic variants             | Highly sensitive for low-frequency variants; adjusts for sequencing errors in quality scores.  |
| Mutect2        | Probabilistic     | Bayesian model with EM (expectation-maximization) | Somatic variants          | Detects tumor variants in tumor-only and tumor-normal modes; optimized for low-frequency variants. |
| Strelka2       | Probabilistic     | Bayesian                                        | Germline and somatic variants| Highly efficient; uses a Bayesian model for somatic variants in tumor-normal; fast and accurate.|
| VarScan2       | Heuristic and Probabilistic | Allele frequency-based model               | Somatic variants             | Very efficient for medium-low coverage; allows adjustable parameters for minimum allele frequencies. |

Due to standard restrictions on software installation in HPC clusters, alternative approaches are provided. The tools used to configure the scripts in CloneSim4Bench will be highlighted. Please take this into account and adjust paths or module loading to align with the resources available on your system.

### FreeBayes

Using prebuilt static binaries

```bash
wget "https://github.com/freebayes/freebayes/releases/download/v1.3.6/freebayes-1.3.6-linux-amd64-static.gz"
gunzip freebayes-1.3.6-linux-amd64-static.gz
chmod +x freebayes-1.3.6-linux-amd64-static
sudo mv freebayes-1.3.6-linux-amd64-static /usr/local/bin/freebayes
freebayes -h
```

Using Advanced Package Tool (APT)

```bash
sudo apt update
sudo apt upgrade
sudo apt install freebayes
freebayes -h
```

Using a Conda Environment

```bash
conda create -n freebayes
conda activate freebayes
conda config --add channels bioconda
conda config --add channels conda-forge
conda install freebayes
freebayes -h
```

**Note**:
-   FreeBayes was installed using APT approach.
-   For further information about the software and its parameters, [click here](FreeBayes.md).

### LoFreq

Cloning the GitHub repository

```
bashgit clone https://github.com/CSB5/lofreq.git
cd lofreq
./bootstrap
lofreq -h
```

Using a Conda Environment

```bash
conda create -n lofreq
conda activate lofreq
conda config --add channels bioconda
conda config --add channels conda-forge
conda install lofreq
lofreq -h
```

**Note**:
-   LoFreq was installed using a Conda Environment.
-   For further information about the software and its parameters, [click here](LoFreq.md).

### GATK Mutect2

Cloning the GitHub repository

```bash
wget "https://github.com/broadinstitute/gatk/releases/download/4.5.0.0/gatk-4.5.0.0.zip"
gunzip -d gatk-4.5.0.0.zip
gatk-4.5.0.0/gatk Mutect2 -h
```

Executing it from a SIF image

```bash
singularity pull docker://broadinstitute/gatk:4.6.0.0
singularity exec gatk_4.5.0.0.sif gatk Mutect2 -h
```
**Note**:
-   GATK Mutect2 was configured for use with the SIF image approach.
-   For further information about the software and its parameters, [click here](docs/Mutect2.md).

### Strelka2

Using the precompiled binaries

```bash
wget “https://github.com/Illumina/strelka/releases/download/v2.9.2/strelka-2.9.2.centos6_x86_64.tar.bz2”
tar xvjf strelka-2.9.2.centos6_x86_64.tar.bz2
bash strelka-2.9.2.centos6_x86_64/bin/runStrelkaSomaticWorkflowDemo.bash
bash strelka-2.9.2.centos6_x86_64/bin/runStrelkaGermlineWorkflowDemo.bash
strelka-2.9.2.centos6_x86_64/bin/configureStrelkaGermlineWorkflow.py
```

Using a Conda environment

```bash
conda create -n strelka2 python=2.7 ipykernel
conda activate strelka2
conda config --add channels bioconda
conda config --add channels conda-forge
conda install strelka2
configureStrelkaGermlineWorkflow.py -h
```
**Note**:
-   Strelka2 was installed using a Conda Environment.
-   For further information about the software and its parameters, [click here](Strelka2.md).

### VarScan2

Cloning the GitHub repository

```bash
git clone https://github.com/dkoboldt/varscan.git
java -jar varscan/VarScan.v2.4.6.jar mpileup2cns
```

**Note**: 
-   VarScan2 was configured for use with the .jar approach.
-   For further information about the software and its parameters, [click here](VarScan2.md).

## Variants Comparison

### BCFTools

BCFtools is a versatile command-line software suite designed for processing and analyzing genetic variant data stored in VCF (Variant Call Format) and BCF (Binary Call Format) files. It provides a comprehensive set of tools for tasks such as file conversion, merging, filtering, and annotation of variants.

BCFtools can be installed using the Advanced Package Tool (APT) on Debian-based systems with the following command:

```bash
sudo apt-get install bcftools
```

### VCFTools

VCFtools is a command-line software package specifically designed for working with VCF (Variant Call Format) files, widely used in the field of genomics for storing genetic variant data. It offers a range of functionalities, including filtering, summarizing, comparing, and converting VCF files. With its focus on flexibility and ease of use, VCFtools enables researchers to extract specific variants, calculate summary statistics, and manage large-scale genomic datasets efficiently.

VCFtools can be installed using the Advanced Package Tool (APT) on Debian-based systems with the following command:

```bash
sudo apt-get install vcftools
```