# LoFreq

## Description

LoFreq also described in 2012, models sequencing error by treating each base in an aligned column as a Bernoulli trial, where success matches the reference base and failure observes a variant. It calculates error probabilities using Phred-scaled quality scores, which represent sequencing error. LoFreq employs a Poisson-binomial distribution to model the probability of observing a certain number of variants in the column. To optimize runtime, LoFreq uses dynamic programming and recursion techniques to compute p-values, while terminating calculations early for non-variant columns.

LoFreq also incorporates sequencing quality by using Phred scores and, if needed, employs an Expectation-Maximization (EM) algorithm to estimate error rates for base substitutions. This allows it to call SNVs even when quality scores are missing or unreliable Wilm et al. (2012).

## Version and Parameters

```bash
version: 2.1.5
commit: unknown
build-date: Jun  8 2024
```

```bash
Usage: lofreq call [options] in.bam

Options:
- Reference:
       -f | --ref FILE              Indexed reference fasta file (gzip supported) [null]
- Output:
       -o | --out FILE              Vcf output file [- = stdout]
- Regions:
       -r | --region STR            Limit calls to this region (chrom:start-end) [null]
       -l | --bed FILE              List of positions (chr pos) or regions (BED) [null]
- Base-call quality:
       -q | --min-bq INT            Skip any base with baseQ smaller than INT [6]
       -Q | --min-alt-bq INT        Skip alternate bases with baseQ smaller than INT [6]
       -R | --def-alt-bq INT        Overwrite baseQs of alternate bases (that passed bq filter) with this value (-1: use median ref-bq; 0: keep) [0]
       -j | --min-jq INT            Skip any base with joinedQ smaller than INT [0]
       -J | --min-alt-jq INT        Skip alternate bases with joinedQ smaller than INT [0]
       -K | --def-alt-jq INT        Overwrite joinedQs of alternate bases (that passed jq filter) with this value (-1: use median ref-bq; 0: keep) [0]
- Base-alignment (BAQ) and indel-aligment (IDAQ) qualities:
       -B | --no-baq                Disable use of base-alignment quality (BAQ)
       -A | --no-idaq               Don't use IDAQ values (NOT recommended under ANY circumstances other than debugging)
       -D | --del-baq               Delete pre-existing BAQ values, i.e. compute even if already present in BAM
       -e | --no-ext-baq            Use 'normal' BAQ (samtools default) instead of extended BAQ (both computed on the fly if not already present in lb tag)
- Mapping quality:
       -m | --min-mq INT            Skip reads with mapping quality smaller than INT [0]
       -M | --max-mq INT            Cap mapping quality at INT [255]
       -N | --no-mq                 Don't merge mapping quality in LoFreq's model
- Indels:
            --call-indels           Enable indel calls (note: preprocess your file to include indel alignment qualities!)
            --only-indels           Only call indels; no SNVs
- Source quality:
       -s | --src-qual              Enable computation of source quality
       -S | --ign-vcf FILE          Ignore variants in this vcf file for source quality computation. Multiple files can be given separated by commas
       -T | --def-nm-q INT          If >= 0, then replace non-match base qualities with this default value [-1]
- P-values:
       -a | --sig                   P-Value cutoff / significance level [0.010000]
       -b | --bonf                  Bonferroni factor. 'dynamic' (increase per actually performed test) or INT ['dynamic']
- Misc.:
       -C | --min-cov INT           Test only positions having at least this coverage [1]
                                    (note: without --no-default-filter default filters (incl. coverage) kick in after predictions are done)
       -d | --max-depth INT         Cap coverage at this depth [1000000]
            --illumina-1.3          Assume the quality is Illumina-1.3-1.7/ASCII+64 encoded
            --use-orphan            Count anomalous read pairs (i.e. where mate is not aligned properly)
            --plp-summary-only      No variant calling. Just output pileup summary per column
            --no-default-filter     Don't run default 'lofreq filter' automatically after calling variants
            --force-overwrite       Overwrite any existing output
            --verbose               Be verbose
            --debug                 Enable debugging
```

## Citation

Wilm A, Aw PP, Bertrand D, Yeo GH, Ong SH, Wong CH, Khor CC, Petric R, Hibberd ML, Nagarajan N. LoFreq: a sequence-quality aware, ultra-sensitive variant caller for uncovering cell-population heterogeneity from high-throughput sequencing datasets. Nucleic Acids Res. 2012 Dec;40(22):11189-201. doi: 10.1093/nar/gks918.