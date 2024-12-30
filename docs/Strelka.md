# Strelka2

## Description

As described in 2018, Strelka2’s algorithm employs a Bayesian model for variant calling, designed to handle both germline and somatic variants. It calculates genotype likelihoods using a probabilistic approach, incorporating empirical error modeling to detect low-frequency variants while distinguishing them from sequencing errors accurately. The algorithm also includes an indel realignment step to correct misalignments near insertions and deletions, improving the accuracy of small indel detection. For efficiency, Strelka2 focuses on “active” genomic regions, and pre-filtering areas with significant variation to optimize computational performance without sacrificing precision.

## Version and Parameters

```bash
Usage: configureStrelkaGermlineWorkflow.py [options]

Version: 2.9.10

This script configures Strelka germline small variant calling.
You must specify an alignment file (BAM or CRAM) for at least one sample.

Configuration will produce a workflow run script which
can execute the workflow on a single node or through
sge and resume any interrupted execution.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --config=FILE         provide a configuration file to override defaults in
                        global config file (/home/arita/.conda/envs/strelka2/s
                        hare/strelka-2.9.10-1/bin/configureStrelkaGermlineWork
                        flow.py.ini)
  --allHelp             show all extended/hidden options

  Workflow options:
    --bam=FILE          Sample BAM or CRAM file. May be specified more than
                        once, multiple inputs will be treated as each BAM file
                        representing a different sample. [required] (no
                        default)
    --ploidy=FILE       Provide ploidy file in VCF. The VCF should include one
                        sample column per input sample labeled with the same
                        sample names found in the input BAM/CRAM RG header
                        sections. Ploidy should be provided in records using
                        the FORMAT/CN field, which are interpreted to span the
                        range [POS+1, INFO/END]. Any CN value besides 1 or 0
                        will be treated as 2. File must be tabix indexed. (no
                        default)
    --noCompress=FILE   Provide BED file of regions where gVCF block
                        compression is not allowed. File must be bgzip-
                        compressed/tabix-indexed. (no default)
    --callContinuousVf=CHROM
                        Call variants on CHROM without a ploidy prior
                        assumption, issuing calls with continuous variant
                        frequencies (no default)
    --rna               Set options for RNA-Seq input.
    --referenceFasta=FILE
                        samtools-indexed reference fasta file [required]
    --indelCandidates=FILE
                        Specify a VCF of candidate indel alleles. These
                        alleles are always evaluated but only reported in the
                        output when they are inferred to exist in the sample.
                        The VCF must be tabix indexed. All indel alleles must
                        be left-shifted/normalized, any unnormalized alleles
                        will be ignored. This option may be specified more
                        than once, multiple input VCFs will be merged.
                        (default: None)
    --forcedGT=FILE     Specify a VCF of candidate alleles. These alleles are
                        always evaluated and reported even if they are
                        unlikely to exist in the sample. The VCF must be tabix
                        indexed. All indel alleles must be left-
                        shifted/normalized, any unnormalized allele will
                        trigger a runtime error. This option may be specified
                        more than once, multiple input VCFs will be merged.
                        Note that for any SNVs provided in the VCF, the SNV
                        site will be reported (and for gVCF, excluded from
                        block compression), but the specific SNV alleles are
                        ignored. (default: None)
    --exome, --targeted
                        Set options for exome or other targeted input: note in
                        particular that this flag turns off high-depth filters
    --callRegions=FILE  Optionally provide a bgzip-compressed/tabix-indexed
                        BED file containing the set of regions to call. No VCF
                        output will be provided outside of these regions. The
                        full genome will still be used to estimate statistics
                        from the input (such as expected depth per
                        chromosome). Only one BED file may be specified.
                        (default: call the entire genome)
    --runDir=DIR        Name of directory to be created where all workflow
                        scripts and output will be written. Each analysis
                        requires a separate directory. (default:
                        StrelkaGermlineWorkflow)
```

## Citation

Kim, Sangtae, Konrad Scheffler, Aaron L. Halpern, Mitchell A. Bekritsky, Eunho Noh, Morten Källberg, Xiaoyu Chen, et al. 2018. “Strelka2: Fast and Accurate Calling of Germline and Somatic Variants.” Nature Methods15 (8): 591–94. <https://doi.org/10.1038/s41592-018-0051-x>.