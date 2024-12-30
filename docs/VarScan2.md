# VarScan2

## Description

VarScan 2 identifies variants by simultaneously analyzing the SAMtools pileup or mpileup output from tumor and normal samples. It performs pairwise comparisons of base calls and sequence depth at each genomic position. The algorithm independently determines the genotype of normal and tumor samples using adjustable thresholds for coverage, base quality, variant allele frequency, and statistical significance. For single-sample variant calling, Fisher’s exact test is employed to distribution based on sequencing error. The default parameters include a minimum coverage of 3x, base quality of 20, a variant allele frequency of 8%, and a P-value threshold of <0.05. Variants with a high allele frequency (≥75%) are called homozygous, while somatic variants are identified by comparing the allele frequencies between tumor and normal samples. VarScan also applies a false-positive filter to reduce sequencing and alignment artifacts.

## Parameters

```bash
USAGE: java -jar VarScan.jar mpileup2cns [pileup file] OPTIONS
        mpileup file - The SAMtools mpileup file
OPTIONS:
        --min-coverage  Minimum read depth at a position to make a call [8]
        --min-reads2    Minimum supporting reads at a position to call variants [2]
        --min-avg-qual  Minimum base quality at a position to count a read [1r5]
        --min-var-freq  Minimum variant allele frequency threshold [0.01]
        --min-freq-for-hom      Minimum frequency to call homozygote [0.75]
        --p-value       Default p-value threshold for calling variants [99e-02]
        --strand-filter Ignore variants with >90% support on one strand [1]
        --output-vcf    If set to 1, outputs in VCF format
        --vcf-sample-list       For VCF output, a list of sample names in order, one per line
        --variants      Report only variant (SNP/indel) positions [0]
```

## Citation

Koboldt, Daniel C., Qunyuan Zhang, David E. Larson, Dong Shen, Michael D. McLellan, Ling Lin, Christopher A. Miller, Elaine R. Mardis, Li Ding, and Richard K. Wilson. 2012. “VarScan 2: Somatic Mutation and Copy Number Alteration Discovery in Cancer by Exome Sequencing.” Genome Research 22 (3): 568–76. <https://doi.org/10.1101/gr.129684.111>.