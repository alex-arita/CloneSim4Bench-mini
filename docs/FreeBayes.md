# FreeBayes

## Description

FreeBayes, first described in 2012, is a haplotype-based variant detection tool that applies a Bayesian statistical framework for population-level inference, particularly suited to detecting variants across multiple samples. At its core, FreeBayes uses Bayes’ theorem to link genotype probabilities with sequencing quality and allele distribution priors in a population. Haplotype observations are dynamically assembled over regions of the genome where multiple alleles vary. These observations come from sequencing reads that map to both ends of the region, and each observation is assigned a quality score, which is factored into the statistical model. FreeBayes then applies a
gradient ascent algorithm to identify the most likely genotypes, ultimately determining whether a given genetic locus contains variation.

This method allows for efficient detection of multiallelic loci and supports non-uniform copy numbers, making it highly versatile for complex variant detection scenarios.

## Installation

Using prebuilt static binaries

<pre><code>wget "https://github.com/freebayes/freebayes/releases/download/v1.3.6/freebayes-1.3.6-linux-amd64-static.gz"
gunzip freebayes-1.3.6-linux-amd64-static.gz
chmod +x freebayes-1.3.6-linux-amd64-static
sudo mv freebayes-1.3.6-linux-amd64-static /usr/local/bin/freebayes
freebayes -h
</code></pre>

Using Advanced Package Tool (APT)

<pre><code>sudo apt update
sudo apt upgrade
sudo apt install freebayes
freebayes -h
</code></pre>

Using a Conda Environment

<pre><code>conda create -n freebayes
conda activate freebayes
conda config --add channels bioconda
conda config --add channels conda-forge
conda install freebayes
freebayes -h
</code></pre>

## Version and Parameters

<pre><code>usage: freebayes -f [REFERENCE] [OPTIONS] [BAM FILES] >[OUTPUT]
&#10;Bayesian haplotype-based polymorphism discovery.
&#10;parameters:
&#10;   -h --help       For a complete description of options.
&#10;freebayes is maintained by Erik Garrison and Pjotr Prins.
&#10;citation: Erik Garrison, Gabor Marth
          "Haplotype-based variant detection from short-read sequencing"
          arXiv:1207.3907 (http://arxiv.org/abs/1207.3907)
&#10;author:   Erik Garrison <erik.garrison@gmail.com>
version:  v1.3.6
&#10;overview:
&#10;    To call variants from aligned short-read sequencing data, supply BAM files and
    a reference.  FreeBayes will provide VCF output on standard out describing SNPs,
    indels, and complex variants in samples in the input alignments.
&#10;    By default, FreeBayes will consider variants supported by at least 2
    observations in a single sample (-C) and also by at least 20% of the reads from
    a single sample (-F).  These settings are suitable to low to high depth
    sequencing in haploid and diploid samples, but users working with polyploid or
    pooled samples may wish to adjust them depending on the characteristics of
    their sequencing data.
&#10;    FreeBayes is capable of calling variant haplotypes shorter than a read length
    where multiple polymorphisms segregate on the same read.  The maximum distance
    between polymorphisms phased in this way is determined by the
    --max-complex-gap, which defaults to 3bp.  In practice, this can comfortably be
    set to half the read length.
&#10;    Ploidy may be set to any level (-p), but by default all samples are assumed to
    be diploid.  FreeBayes can model per-sample and per-region variation in
    copy-number (-A) using a copy-number variation map.
&#10;    FreeBayes can act as a frequency-based pooled caller and describe variants
    and haplotypes in terms of observation frequency rather than called genotypes.
    To do so, use --pooled-continuous and set input filters to a suitable level.
    Allele observation counts will be described by AO and RO fields in the VCF output.
&#10;
examples:
&#10;    # call variants assuming a diploid sample
    freebayes -f ref.fa aln.bam >var.vcf
&#10;    # call variants assuming a diploid sample, providing gVCF output
    freebayes -f ref.fa --gvcf aln.bam >var.gvcf
&#10;    # require at least 5 supporting observations to consider a variant
    freebayes -f ref.fa -C 5 aln.bam >var.vcf
&#10;    # discard alignments overlapping positions where total read depth is greater than 200
    freebayes -f ref.fa -g 200 aln.bam >var.vcf
&#10;    # use a different ploidy
    freebayes -f ref.fa -p 4 aln.bam >var.vcf
&#10;    # assume a pooled sample with a known number of genome copies
    freebayes -f ref.fa -p 20 --pooled-discrete aln.bam >var.vcf
&#10;    # generate frequency-based calls for all variants passing input thresholds
    freebayes -f ref.fa -F 0.01 -C 1 --pooled-continuous aln.bam >var.vcf
&#10;    # use an input VCF (bgzipped + tabix indexed) to force calls at particular alleles
    freebayes -f ref.fa -@ in.vcf.gz aln.bam >var.vcf
&#10;    # generate long haplotype calls over known variants
    freebayes -f ref.fa --haplotype-basis-alleles in.vcf.gz \
                        --haplotype-length 50 aln.bam
&#10;    # naive variant calling: simply annotate observation counts of SNPs and indels
    freebayes -f ref.fa --haplotype-length 0 --min-alternate-count 1 \
        --min-alternate-fraction 0 --pooled-continuous --report-monomorphic aln.bam >var.vcf
&#10;
parameters:
&#10;   -h --help       Prints this help dialog.
   --version       Prints the release number and the git commit id.
&#10;input:
&#10;   -b --bam FILE   Add FILE to the set of BAM files to be analyzed.
   -L --bam-list FILE
                   A file containing a list of BAM files to be analyzed.
   -c --stdin      Read BAM input on stdin.
   -f --fasta-reference FILE
                   Use FILE as the reference sequence for analysis.
                   An index file (FILE.fai) will be created if none exists.
                   If neither --targets nor --region are specified, FreeBayes
                   will analyze every position in this reference.
   -t --targets FILE
                   Limit analysis to targets listed in the BED-format FILE.
   -r --region <chrom>:<start_position>-<end_position>
                   Limit analysis to the specified region, 0-base coordinates,
                   end_position not included (same as BED format).
                   Either '-' or '..' maybe used as a separator.
   -s --samples FILE
                   Limit analysis to samples listed (one per line) in the FILE.
                   By default FreeBayes will analyze all samples in its input
                   BAM files.
   --populations FILE
                   Each line of FILE should list a sample and a population which
                   it is part of.  The population-based bayesian inference model
                   will then be partitioned on the basis of the populations.
   -A --cnv-map FILE
                   Read a copy number map from the BED file FILE, which has
                   either a sample-level ploidy:
                      sample_name copy_number
                   or a region-specific format:
                      seq_name start end sample_name copy_number
                   ... for each region in each sample which does not have the
                   default copy number as set by --ploidy. These fields can be delimited
                   by space or tab.
&#10;output:
&#10;   -v --vcf FILE   Output VCF-format results to FILE. (default: stdout)
   --gvcf
                   Write gVCF output, which indicates coverage in uncalled regions.
   --gvcf-chunk NUM
                   When writing gVCF output emit a record for every NUM bases.
   -& --gvcf-dont-use-chunk BOOL
                   When writing the gVCF output emit a record for all bases if
                   set to "true" , will also route an int to --gvcf-chunk
                   similar to --output-mode EMIT_ALL_SITES from GATK
   -@ --variant-input VCF
                   Use variants reported in VCF file as input to the algorithm.
                   Variants in this file will included in the output even if
                   there is not enough support in the data to pass input filters.
   -l --only-use-input-alleles
                   Only provide variant calls and genotype likelihoods for sites
                   and alleles which are provided in the VCF input, and provide
                   output in the VCF for all input alleles, not just those which
                   have support in the data.
   --haplotype-basis-alleles VCF
                   When specified, only variant alleles provided in this input
                   VCF will be used for the construction of complex or haplotype
                   alleles.
   --report-all-haplotype-alleles
                   At sites where genotypes are made over haplotype alleles,
                   provide information about all alleles in output, not only
                   those which are called.
   --report-monomorphic
                   Report even loci which appear to be monomorphic, and report all
                   considered alleles, even those which are not in called genotypes.
                   Loci which do not have any potential alternates have '.' for ALT.
   -P --pvar N     Report sites if the probability that there is a polymorphism
                   at the site is greater than N.  default: 0.0.  Note that post-
                   filtering is generally recommended over the use of this parameter.
   --strict-vcf
                   Generate strict VCF format (FORMAT/GQ will be an int)
&#10;population model:
&#10;   -T --theta N    The expected mutation rate or pairwise nucleotide diversity
                   among the population under analysis.  This serves as the
                   single parameter to the Ewens Sampling Formula prior model
                   default: 0.001
   -p --ploidy N   Sets the default ploidy for the analysis to N.  default: 2
   -J --pooled-discrete
                   Assume that samples result from pooled sequencing.
                   Model pooled samples using discrete genotypes across pools.
                   When using this flag, set --ploidy to the number of
                   alleles in each sample or use the --cnv-map to define
                   per-sample ploidy.
   -K --pooled-continuous
                   Output all alleles which pass input filters, regardles of
                   genotyping outcome or model.
&#10;reference allele:
&#10;   -Z --use-reference-allele
                   This flag includes the reference allele in the analysis as
                   if it is another sample from the same population.
   --reference-quality MQ,BQ
                   Assign mapping quality of MQ to the reference allele at each
                   site and base quality of BQ.  default: 100,60
&#10;allele scope:
&#10;   -n --use-best-n-alleles N
                   Evaluate only the best N SNP alleles, ranked by sum of
                   supporting quality scores.  (Set to 0 to use all; default: all)
   -E --max-complex-gap N
      --haplotype-length N
                   Allow haplotype calls with contiguous embedded matches of up
                   to this length. Set N=-1 to disable clumping. (default: 3)
   --min-repeat-size N
                   When assembling observations across repeats, require the total repeat
                   length at least this many bp.  (default: 5)
   --min-repeat-entropy N
                   To detect interrupted repeats, build across sequence until it has
                   entropy > N bits per bp. Set to 0 to turn off. (default: 1)
   --no-partial-observations
                   Exclude observations which do not fully span the dynamically-determined
                   detection window.  (default, use all observations, dividing partial
                   support across matching haplotypes when generating haplotypes.)
&#10;  These flags are meant for testing.
  They are not meant for filtering the output.
  They actually filter the input to the algorithm by throwing away alignments.
  This hurts performance by hiding information from the Bayesian model.
  Do not use them unless you can validate that they improve results!
&#10;   -I --throw-away-snp-obs     Remove SNP observations from input.
   -i --throw-away-indels-obs  Remove indel observations from input.
   -X --throw-away-mnp-obs     Remove MNP observations from input.
   -u --throw-away-complex-obs Remove complex allele observations from input.
&#10;  If you need to break apart haplotype calls to obtain one class of alleles,
  run the call with default parameters, then normalize and subset the VCF:
    freebayes ... | vcfallelicprimitives -kg >calls.vcf
  For example, this would retain only biallelic SNPs.
    <calls.vcf vcfsnps | vcfbiallelic >biallelic_snp_calls.vcf
&#10;indel realignment:
&#10;   -O --dont-left-align-indels
                   Turn off left-alignment of indels, which is enabled by default.
&#10;input filters:
&#10;   -4 --use-duplicate-reads
                   Include duplicate-marked alignments in the analysis.
                   default: exclude duplicates marked as such in alignments
   -m --min-mapping-quality Q
                   Exclude alignments from analysis if they have a mapping
                   quality less than Q.  default: 1
   -q --min-base-quality Q
                   Exclude alleles from analysis if their supporting base
                   quality is less than Q.  default: 0
   -R --min-supporting-allele-qsum Q
                   Consider any allele in which the sum of qualities of supporting
                   observations is at least Q.  default: 0
   -Y --min-supporting-mapping-qsum Q
                   Consider any allele in which and the sum of mapping qualities of
                   supporting reads is at least Q.  default: 0
   -Q --mismatch-base-quality-threshold Q
                   Count mismatches toward --read-mismatch-limit if the base
                   quality of the mismatch is >= Q.  default: 10
   -U --read-mismatch-limit N
                   Exclude reads with more than N mismatches where each mismatch
                   has base quality >= mismatch-base-quality-threshold.
                   default: ~unbounded
   -z --read-max-mismatch-fraction N
                   Exclude reads with more than N [0,1] fraction of mismatches where
                   each mismatch has base quality >= mismatch-base-quality-threshold
                   default: 1.0
   -$ --read-snp-limit N
                   Exclude reads with more than N base mismatches, ignoring gaps
                   with quality >= mismatch-base-quality-threshold.
                   default: ~unbounded
   -e --read-indel-limit N
                   Exclude reads with more than N separate gaps.
                   default: ~unbounded
   -0 --standard-filters  Use stringent input base and mapping quality filters
                   Equivalent to -m 30 -q 20 -R 0 -S 0
   -F --min-alternate-fraction N
                   Require at least this fraction of observations supporting
                   an alternate allele within a single individual in the
                   in order to evaluate the position.  default: 0.05
   -C --min-alternate-count N
                   Require at least this count of observations supporting
                   an alternate allele within a single individual in order
                   to evaluate the position.  default: 2
   -3 --min-alternate-qsum N
                   Require at least this sum of quality of observations supporting
                   an alternate allele within a single individual in order
                   to evaluate the position.  default: 0
   -G --min-alternate-total N
                   Require at least this count of observations supporting
                   an alternate allele within the total population in order
                   to use the allele in analysis.  default: 1
   --min-coverage N
                   Require at least this coverage to process a site. default: 0
   --limit-coverage N
                   Downsample per-sample coverage to this level if greater than this coverage.
                   default: no limit
   -g --skip-coverage N
                   Skip processing of alignments overlapping positions with coverage >N.
                   This filters sites above this coverage, but will also reduce data nearby.
                   default: no limit
   --trim-complex-tail
                   Trim complex tails.
&#10;population priors:
&#10;   -k --no-population-priors
                   Equivalent to --pooled-discrete --hwe-priors-off and removal of
                   Ewens Sampling Formula component of priors.
&#10;mappability priors:
&#10;   -w --hwe-priors-off
                   Disable estimation of the probability of the combination
                   arising under HWE given the allele frequency as estimated
                   by observation frequency.
   -V --binomial-obs-priors-off
                   Disable incorporation of prior expectations about observations.
                   Uses read placement probability, strand balance probability,
                   and read position (5'-3') probability.
   -a --allele-balance-priors-off
                   Disable use of aggregate probability of observation balance between alleles
                   as a component of the priors.
&#10;genotype likelihoods:
&#10;   --observation-bias FILE
                   Read length-dependent allele observation biases from FILE.
                   The format is [length] [alignment efficiency relative to reference]
                   where the efficiency is 1 if there is no relative observation bias.
   --base-quality-cap Q
                   Limit estimated observation quality by capping base quality at Q.
   --prob-contamination F
                   An estimate of contamination to use for all samples.  default: 10e-9
   --legacy-gls    Use legacy (polybayes equivalent) genotype likelihood calculations
   --contamination-estimates FILE
                   A file containing per-sample estimates of contamination, such as
                   those generated by VerifyBamID.  The format should be:
                       sample p(read=R|genotype=AR) p(read=A|genotype=AA)
                   Sample '*' can be used to set default contamination estimates.
&#10;algorithmic features:
&#10;   --report-genotype-likelihood-max
                   Report genotypes using the maximum-likelihood estimate provided
                   from genotype likelihoods.
   -B --genotyping-max-iterations N
                   Iterate no more than N times during genotyping step. default: 1000.
   --genotyping-max-banddepth N
                   Integrate no deeper than the Nth best genotype by likelihood when
                   genotyping. default: 6.
   -W --posterior-integration-limits N,M
                   Integrate all genotype combinations in our posterior space
                   which include no more than N samples with their Mth best
                   data likelihood. default: 1,3.
   -N --exclude-unobserved-genotypes
                   Skip sample genotypings for which the sample has no supporting reads.
   -S --genotype-variant-threshold N
                   Limit posterior integration to samples where the second-best
                   genotype likelihood is no more than log(N) from the highest
                   genotype likelihood for the sample.  default: ~unbounded
   -j --use-mapping-quality
                   Use mapping quality of alleles when calculating data likelihoods.
   -H --harmonic-indel-quality
                   Use a weighted sum of base qualities around an indel, scaled by the
                   distance from the indel.  By default use a minimum BQ in flanking sequence.
   -D --read-dependence-factor N
                   Incorporate non-independence of reads by scaling successive
                   observations by this factor during data likelihood
                   calculations.  default: 0.9
   -= --genotype-qualities
                   Calculate the marginal probability of genotypes and report as GQ in
                   each sample field in the VCF output.
&#10;debugging:
&#10;   -d --debug      Print debugging output.
   -dd             Print more verbose debugging output (requires "make DEBUG")
&#10;
author:   Erik Garrison <erik.garrison@gmail.com>
version:  v1.3.6
</code></pre>

<div id="refs" class="references csl-bib-body hanging-indent"
entry-spacing="0">

<div id="ref-Garrison.1772012" class="csl-entry">

Garrison, Erik, and Gabor Marth. n.d. “Haplotype-Based Variant Detection
from Short-Read Sequencing.” <http://arxiv.org/pdf/1207.3907>.

</div>

</div>
