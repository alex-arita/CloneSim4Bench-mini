# GATK Mutect2

## Description

Mutect2 algorithm differs from the one used in Mutect. This new implementation is based on the algorithm behind HaplotypeCaller by GATK which uses theoretical haplotypes based on de Bruijn-like graphs from a consensus of the reads covering the genomic region. HaplotypeCaller focuses variants calling on “ActiveRegions,” which are parts of the genome that show significant differences from the reference sequence.

These regions are identified based on signs of disagreement, such as base mismatches, insertions, deletions, or soft-clipped reads with high base quality. Within these regions, reads are broken into overlapping sequences (k-mers) and reassembled into candidate haplotypes using a de-Bruijn-like graph. A pair-HMM (Hidden Markov Model) is then built using base quality information to calculate the likelihood of each read originating from each haplotype. These likelihoods are used to estimate genotype probabilities, which are ultimately used to call variants across the sample cohort.

## Version and Parameters

```bash
Call somatic SNVs and indels via local assembly of haplotypes
Version:4.5.0.0


Required Arguments:

--input,-I <GATKPath>         BAM/SAM/CRAM file containing reads  This argument must be specified at least once.
                              Required. 

--output,-O <GATKPath>        File to which variants should be written  Required. 

--reference,-R <GATKPath>     Reference sequence file  Required. 


Optional Arguments:

--add-output-sam-program-record <Boolean>
                              If true, adds a PG tag to created SAM/BAM/CRAM files.  Default value: true. Possible
                              values: {true, false} 

--add-output-vcf-command-line <Boolean>
                              If true, adds a command line header line to created VCF files.  Default value: true.
                              Possible values: {true, false} 

--af-of-alleles-not-in-resource,-default-af <Double>
                              Population allele fraction assigned to alleles not found in germline resource.  Please see
                              docs/mutect/mutect2.pdf fora derivation of the default value.  Default value: -1.0. 

--alleles <FeatureInput>      The set of alleles to force-call regardless of evidence  Default value: null. 

--annotation,-A <String>      One or more specific annotations to add to variant calls  This argument may be specified 0
                              or more times. Default value: null. Possible values: {AlleleFraction, AllelePseudoDepth,
                              AS_BaseQualityRankSumTest, AS_FisherStrand, AS_InbreedingCoeff,
                              AS_MappingQualityRankSumTest, AS_QualByDepth, AS_ReadPosRankSumTest, AS_RMSMappingQuality,
                              AS_StrandBiasMutectAnnotation, AS_StrandOddsRatio, AssemblyComplexity, BaseQuality,
                              BaseQualityHistogram, BaseQualityRankSumTest, ChromosomeCounts, ClippingRankSumTest,
                              CountNs, Coverage, CycleSkipStatus, DepthPerAlleleBySample, DepthPerSampleHC, ExcessHet,
                              FeaturizedReadSets, FisherStrand, FragmentDepthPerAlleleBySample, FragmentLength,
                              GcContent, GenotypeSummaries, HaplotypeFilteringAnnotation, HmerIndelLength, HmerIndelNuc,
                              HmerMotifs, InbreedingCoeff, IndelClassify, IndelLength, LikelihoodRankSumTest,
                              MappingQuality, MappingQualityRankSumTest, MappingQualityZero, OrientationBiasReadCounts,
                              OriginalAlignment, PossibleDeNovo, QualByDepth, RawGtCount, ReadPosition,
                              ReadPosRankSumTest, ReferenceBases, RMSMappingQuality, SampleList, StrandBiasBySample,
                              StrandOddsRatio, TandemRepeat, TransmittedSingleton, UniqueAltReadCount, VariantType} 

--annotation-group,-G <String>One or more groups of annotations to apply to variant calls  This argument may be
                              specified 0 or more times. Default value: null. Possible values:
                              {AlleleSpecificAnnotation, AS_StandardAnnotation, GenotypeAnnotation, InfoFieldAnnotation,
                              JumboGenotypeAnnotation, JumboInfoAnnotation, ReducibleAnnotation, StandardAnnotation,
                              StandardFlowBasedAnnotation, StandardHCAnnotation, StandardMutectAnnotation,
                              VariantAnnotation} 

--annotations-to-exclude,-AX <String>
                              One or more specific annotations to exclude from variant calls  This argument may be
                              specified 0 or more times. Default value: null. Possible values:
                              {AS_StrandBiasMutectAnnotation, BaseQuality, Coverage, DepthPerAlleleBySample,
                              DepthPerSampleHC, FragmentDepthPerAlleleBySample, FragmentLength, MappingQuality,
                              OrientationBiasReadCounts, ReadPosition, StrandBiasBySample, TandemRepeat} 

--arguments_file <File>       read one or more arguments files and add them to the command line  This argument may be
                              specified 0 or more times. Default value: null. 

--assembly-region-out <String>Output the assembly region to this IGV formatted file  Default value: null. 

--assembly-region-padding <Integer>
                              Number of additional bases of context to include around each assembly region  Default
                              value: 100. 

--base-quality-score-threshold <Byte>
                              Base qualities below this threshold will be reduced to the minimum (6)  Default value: 18.

--callable-depth <Integer>    Minimum depth to be considered callable for Mutect stats.  Does not affect genotyping. 
                              Default value: 10. 

--cloud-index-prefetch-buffer,-CIPB <Integer>
                              Size of the cloud-only prefetch buffer (in MB; 0 to disable). Defaults to
                              cloudPrefetchBuffer if unset.  Default value: -1. 

--cloud-prefetch-buffer,-CPB <Integer>
                              Size of the cloud-only prefetch buffer (in MB; 0 to disable).  Default value: 40. 

--create-output-bam-index,-OBI <Boolean>
                              If true, create a BAM/CRAM index when writing a coordinate-sorted BAM/CRAM file.  Default
                              value: true. Possible values: {true, false} 

--create-output-bam-md5,-OBM <Boolean>
                              If true, create a MD5 digest for any BAM/SAM/CRAM file created  Default value: false.
                              Possible values: {true, false} 

--create-output-variant-index,-OVI <Boolean>
                              If true, create a VCF index when writing a coordinate-sorted VCF file.  Default value:
                              true. Possible values: {true, false} 

--create-output-variant-md5,-OVM <Boolean>
                              If true, create a a MD5 digest any VCF file created.  Default value: false. Possible
                              values: {true, false} 

--disable-bam-index-caching,-DBIC <Boolean>
                              If true, don't cache bam indexes, this will reduce memory requirements but may harm
                              performance if many intervals are specified.  Caching is automatically disabled if there
                              are no intervals specified.  Default value: false. Possible values: {true, false} 

--disable-read-filter,-DF <String>
                              Read filters to be disabled before analysis  This argument may be specified 0 or more
                              times. Default value: null. Possible values: {GoodCigarReadFilter, MappedReadFilter,
                              MappingQualityAvailableReadFilter, MappingQualityNotZeroReadFilter,
                              MappingQualityReadFilter, NonChimericOriginalAlignmentReadFilter,
                              NonZeroReferenceLengthAlignmentReadFilter, NotDuplicateReadFilter,
                              NotSecondaryAlignmentReadFilter, PassesVendorQualityCheckReadFilter, ReadLengthReadFilter,
                              WellformedReadFilter} 

--disable-sequence-dictionary-validation <Boolean>
                              If specified, do not check the sequence dictionaries from our inputs for compatibility.
                              Use at your own risk!  Default value: false. Possible values: {true, false} 

--dont-use-dragstr-pair-hmm-scores <Boolean>
                              disable DRAGstr pair-hmm score even when dragstr-params-path was provided  Default value:
                              false. Possible values: {true, false} 

--dont-use-soft-clipped-bases <Boolean>
                              Do not analyze soft clipped bases in the reads  Default value: false. Possible values:
                              {true, false} 

--downsampling-stride,-stride <Integer>
                              Downsample a pool of reads starting within a range of one or more bases.  Default value:
                              1. 

--dragstr-het-hom-ratio <Integer>
                              het to hom prior ratio use with DRAGstr on  Default value: 2. 

--dragstr-params-path <GATKPath>
                              location of the DRAGstr model parameters for STR error correction used in the Pair HMM.
                              When provided, it overrides other PCR error correcting mechanisms  Default value: null. 

--enable-dynamic-read-disqualification-for-genotyping <Boolean>
                              Will enable less strict read disqualification low base quality reads  Default value:
                              false. Possible values: {true, false} 

--exclude-intervals,-XL <String>
                              One or more genomic intervals to exclude from processing  This argument may be specified 0
                              or more times. Default value: null. 

--f1r2-max-depth <Integer>    sites with depth higher than this value will be grouped  Default value: 200. 

--f1r2-median-mq <Integer>    skip sites with median mapping quality below this value  Default value: 50. 

--f1r2-min-bq <Integer>       exclude bases below this quality from pileup  Default value: 20. 

--f1r2-tar-gz <File>          If specified, collect F1R2 counts and output files into this tar.gz file  Default value:
                              null. 

--flow-order-for-annotations <String>
                              flow order used for this annotations. [readGroup:]flowOrder  This argument may be
                              specified 0 or more times. Default value: null. 

--founder-id <String>         Samples representing the population "founders"  This argument may be specified 0 or more
                              times. Default value: null. 

--gatk-config-file <String>   A configuration file to use with the GATK.  Default value: null. 

--gcs-max-retries,-gcs-retries <Integer>
                              If the GCS bucket channel errors out, how many times it will attempt to re-initiate the
                              connection  Default value: 20. 

--gcs-project-for-requester-pays <String>
                              Project to bill when accessing "requester pays" buckets. If unset, these buckets cannot be
                              accessed.  User must have storage.buckets.get permission on the bucket being accessed. 
                              Default value: . 

--genotype-germline-sites <Boolean>
                              Call all apparent germline site even though they will ultimately be filtered.  Default
                              value: false. Possible values: {true, false} 

--genotype-pon-sites <Boolean>Call sites in the PoN even though they will ultimately be filtered.  Default value: false.
                              Possible values: {true, false} 

--germline-resource <FeatureInput>
                              Population vcf of germline sequencing containing allele fractions.  Default value: null. 

--graph-output,-graph <String>Write debug assembly graph information to this file  Default value: null. 

--help,-h <Boolean>           display the help message  Default value: false. Possible values: {true, false} 

--ignore-itr-artifacts <Boolean>
                              Turn off read transformer that clips artifacts associated with end repair insertions near
                              inverted tandem repeats.  Default value: false. Possible values: {true, false} 

--initial-tumor-lod,-init-lod <Double>
                              Log 10 odds threshold to consider pileup active.  Default value: 2.0. 

--interval-exclusion-padding,-ixp <Integer>
                              Amount of padding (in bp) to add to each interval you are excluding.  Default value: 0. 

--interval-merging-rule,-imr <IntervalMergingRule>
                              Interval merging rule for abutting intervals  Default value: ALL. Possible values: {ALL,
                              OVERLAPPING_ONLY} 

--interval-padding,-ip <Integer>
                              Amount of padding (in bp) to add to each interval you are including.  Default value: 0. 

--interval-set-rule,-isr <IntervalSetRule>
                              Set merging approach to use for combining interval inputs  Default value: UNION. Possible
                              values: {UNION, INTERSECTION} 

--intervals,-L <String>       One or more genomic intervals over which to operate  This argument may be specified 0 or
                              more times. Default value: null. 

--lenient,-LE <Boolean>       Lenient processing of VCF files  Default value: false. Possible values: {true, false} 

--max-assembly-region-size <Integer>
                              Maximum size of an assembly region  Default value: 300. 

--max-population-af,-max-af <Double>
                              Maximum population allele frequency in tumor-only mode.  Default value: 0.01. 

--max-reads-per-alignment-start <Integer>
                              Maximum number of reads to retain per alignment start position. Reads above this threshold
                              will be downsampled. Set to 0 to disable.  Default value: 50. 

--max-variants-per-shard <Integer>
                              If non-zero, partitions VCF output into shards, each containing up to the given number of
                              records.  Default value: 0. 

--min-assembly-region-size <Integer>
                              Minimum size of an assembly region  Default value: 50. 

--min-base-quality-score,-mbq <Byte>
                              Minimum base quality required to consider a base for calling  Default value: 10. 

--mitochondria-mode <Boolean> Mitochondria mode sets emission and initial LODs to 0.  Default value: false. Possible
                              values: {true, false} 

--mutect3-alt-downsample <Integer>
                              Downsample alt reads to this count for Mutect3 training datasets.  Default value: 20. 

--mutect3-dataset <File>      Destination for Mutect3 data collection  Default value: null. 

--mutect3-non-artifact-ratio <Integer>
                              Number of non-artifact data per artifact datum in Mutect3 training.  Default value: 20. 

--mutect3-ref-downsample <Integer>
                              Downsample ref reads to this count when generating a Mutect3 dataset.  Default value: 10. 

--mutect3-training-mode <Boolean>
                              Collect Mutect3 data for learning.  Default value: false. Possible values: {true, false} 

--mutect3-training-truth <FeatureInput>
                              VCF file of known variants for labeling Mutect3 training data  Default value: null. 

--native-pair-hmm-threads <Integer>
                              How many threads should a native pairHMM implementation use  Default value: 4. 

--native-pair-hmm-use-double-precision <Boolean>
                              use double precision in the native pairHmm. This is slower but matches the java
                              implementation better  Default value: false. Possible values: {true, false} 

--normal-lod <Double>         Log 10 odds threshold for calling normal variant non-germline.  Default value: 2.2. 

--normal-sample,-normal <String>
                              BAM sample name of normal(s), if any.  May be URL-encoded as output by GetSampleName with
                              -encode argument.  This argument may be specified 0 or more times. Default value: null. 

--panel-of-normals,-pon <FeatureInput>
                              VCF file of sites observed in normal.  Default value: null. 

--pcr-indel-qual <Integer>    Phred-scaled PCR indel qual for overlapping fragments  Default value: 40. 

--pcr-snv-qual <Integer>      Phred-scaled PCR SNV qual for overlapping fragments  Default value: 40. 

--pedigree,-ped <GATKPath>    Pedigree file for determining the population "founders"  Default value: null. 

--QUIET <Boolean>             Whether to suppress job-summary info on System.err.  Default value: false. Possible
                              values: {true, false} 

--read-filter,-RF <String>    Read filters to be applied before analysis  This argument may be specified 0 or more
                              times. Default value: null. Possible values: {AlignmentAgreesWithHeaderReadFilter,
                              AllowAllReadsReadFilter, AmbiguousBaseReadFilter, CigarContainsNoNOperator,
                              ExcessiveEndClippedReadFilter, FirstOfPairReadFilter,
                              FlowBasedTPAttributeSymetricReadFilter, FlowBasedTPAttributeValidReadFilter,
                              FragmentLengthReadFilter, GoodCigarReadFilter, HasReadGroupReadFilter,
                              HmerQualitySymetricReadFilter, IntervalOverlapReadFilter,
                              JexlExpressionReadTagValueFilter, LibraryReadFilter, MappedReadFilter,
                              MappingQualityAvailableReadFilter, MappingQualityNotZeroReadFilter,
                              MappingQualityReadFilter, MatchingBasesAndQualsReadFilter, MateDifferentStrandReadFilter,
                              MateDistantReadFilter, MateOnSameContigOrNoMappedMateReadFilter,
                              MateUnmappedAndUnmappedReadFilter, MetricsReadFilter,
                              NonChimericOriginalAlignmentReadFilter, NonZeroFragmentLengthReadFilter,
                              NonZeroReferenceLengthAlignmentReadFilter, NotDuplicateReadFilter,
                              NotOpticalDuplicateReadFilter, NotProperlyPairedReadFilter,
                              NotSecondaryAlignmentReadFilter, NotSupplementaryAlignmentReadFilter,
                              OverclippedReadFilter, PairedReadFilter, PassesVendorQualityCheckReadFilter,
                              PlatformReadFilter, PlatformUnitReadFilter, PrimaryLineReadFilter,
                              ProperlyPairedReadFilter, ReadGroupBlackListReadFilter, ReadGroupHasFlowOrderReadFilter,
                              ReadGroupReadFilter, ReadLengthEqualsCigarLengthReadFilter, ReadLengthReadFilter,
                              ReadNameReadFilter, ReadStrandFilter, ReadTagValueFilter, SampleReadFilter,
                              SecondOfPairReadFilter, SeqIsStoredReadFilter, SoftClippedReadFilter,
                              ValidAlignmentEndReadFilter, ValidAlignmentStartReadFilter, WellformedFlowBasedReadFilter,
                              WellformedReadFilter} 

--read-index <GATKPath>       Indices to use for the read inputs. If specified, an index must be provided for every read
                              input and in the same order as the read inputs. If this argument is not specified, the
                              path to the index for each input will be inferred automatically.  This argument may be
                              specified 0 or more times. Default value: null. 

--read-validation-stringency,-VS <ValidationStringency>
                              Validation stringency for all SAM/BAM/CRAM/SRA files read by this program.  The default
                              stringency value SILENT can improve performance when processing a BAM file in which
                              variable-length data (read, qualities, tags) do not otherwise need to be decoded.  Default
                              value: SILENT. Possible values: {STRICT, LENIENT, SILENT} 

--seconds-between-progress-updates <Double>
                              Output traversal statistics every time this many seconds elapse  Default value: 10.0. 

--sequence-dictionary <GATKPath>
                              Use the given sequence dictionary as the master/canonical sequence dictionary.  Must be a
                              .dict file.  Default value: null. 

--sites-only-vcf-output <Boolean>
                              If true, don't emit genotype fields when writing vcf file output.  Default value: false.
                              Possible values: {true, false} 

--tmp-dir <GATKPath>          Temp directory to use.  Default value: null. 

--tumor-lod-to-emit,-emit-lod <Double>
                              Log 10 odds threshold to emit variant to VCF.  Default value: 3.0. 

--tumor-sample,-tumor <String>This argument is DEPRECATED (This feature is deprecated and will be removed in a future
                              release.). BAM sample name of tumor.  May be URL-encoded as output by GetSampleName with
                              -encode argument.  Default value: null. 

--use-jdk-deflater,-jdk-deflater <Boolean>
                              Whether to use the JdkDeflater (as opposed to IntelDeflater)  Default value: false.
                              Possible values: {true, false} 

--use-jdk-inflater,-jdk-inflater <Boolean>
                              Whether to use the JdkInflater (as opposed to IntelInflater)  Default value: false.
                              Possible values: {true, false} 

--use-pdhmm <Boolean>         Partially Determined HMM, an alternative to the regular assembly haplotypes where we
                              instead construct artificial haplotypes out of the union of the assembly and pileup
                              alleles.  Default value: false. Possible values: {true, false} 

--verbosity <LogLevel>        Control verbosity of logging.  Default value: INFO. Possible values: {ERROR, WARNING,
                              INFO, DEBUG} 

--version <Boolean>           display the version number for this tool  Default value: false. Possible values: {true,
                              false} 


Advanced Arguments:

--active-probability-threshold <Double>
                              Minimum probability for a locus to be considered active.  Default value: 0.002. 

--adaptive-pruning-initial-error-rate <Double>
                              Initial base error rate estimate for adaptive pruning  Default value: 0.001. 

--allele-informative-reads-overlap-margin <Integer>
                              Likelihood and read-based annotations will only take into consideration reads that overlap
                              the variant or any base no further than this distance expressed in base pairs  Default
                              value: 2. 

--allow-non-unique-kmers-in-ref <Boolean>
                              Allow graphs that have non-unique kmers in the reference  Default value: false. Possible
                              values: {true, false} 

--bam-output,-bamout <String> File to which assembled haplotypes should be written  Default value: null. 

--bam-writer-type <WriterType>Which haplotypes should be written to the BAM  Default value: CALLED_HAPLOTYPES. Possible
                              values: {ALL_POSSIBLE_HAPLOTYPES, CALLED_HAPLOTYPES, NO_HAPLOTYPES,
                              CALLED_HAPLOTYPES_NO_READS} 

--base-qual-correction-factor <Integer>
                              Set to zero to turn off the error model changes included in GATK 4.1.9.0.  Default value:
                              5. 

--debug-assembly,-debug <Boolean>
                              Print out verbose debug information about each assembly region  Default value: false.
                              Possible values: {true, false} 

--disable-adaptive-pruning <Boolean>
                              Disable the adaptive algorithm for pruning paths in the graph  Default value: false.
                              Possible values: {true, false} 

--disable-cap-base-qualities-to-map-quality <Boolean>
                              If false this disables capping of base qualities in the HMM to the mapping quality of the
                              read  Default value: false. Possible values: {true, false} 

--disable-symmetric-hmm-normalizing <Boolean>
                              Toggle to revive legacy behavior of asymmetrically normalizing the arguments to the
                              reference haplotype  Default value: false. Possible values: {true, false} 

--disable-tool-default-annotations <Boolean>
                              Disable all tool default annotations  Default value: false. Possible values: {true, false}

--disable-tool-default-read-filters <Boolean>
                              Disable all tool default read filters (WARNING: many tools will not function correctly
                              without their default read filters on)  Default value: false. Possible values: {true,
                              false} 

--dont-increase-kmer-sizes-for-cycles <Boolean>
                              Disable iterating over kmer sizes when graph cycles are detected  Default value: false.
                              Possible values: {true, false} 

--emit-ref-confidence,-ERC <ReferenceConfidenceMode>
                              Mode for emitting reference confidence scores (For Mutect2, this is a BETA feature) 
                              Default value: NONE. Possible values: {NONE, BP_RESOLUTION, GVCF} 

--enable-all-annotations <Boolean>
                              Use all possible annotations (not for the faint of heart)  Default value: false. Possible
                              values: {true, false} 

--expected-mismatch-rate-for-read-disqualification <Double>
                              Error rate used to set expectation for post HMM read disqualification based on mismatches 
                              Default value: 0.02. 

--flow-assembly-collapse-partial-mode <Boolean>
                              Collapse long flow-based hmers only up to difference in reference  Default value: false.
                              Possible values: {true, false} 

--flow-disallow-probs-larger-than-call <Boolean>
                              Cap probabilities of error to 1 relative to base call  Default value: false. Possible
                              values: {true, false} 

--flow-fill-empty-bins-value <Double>
                              Value to fill the zeros of the matrix with  Default value: 0.001. 

--flow-filter-alleles <Boolean>
                              pre-filter alleles before genotyping  Default value: false. Possible values: {true, false}

--flow-filter-alleles-qual-threshold <Float>
                              Threshold for prefiltering alleles on quality  Default value: 30.0. 

--flow-filter-alleles-sor-threshold <Float>
                              Threshold for prefiltering alleles on SOR  Default value: 3.0. 

--flow-filter-lone-alleles <Boolean>
                              Remove also lone alleles during allele filtering  Default value: false. Possible values:
                              {true, false} 

--flow-lump-probs <Boolean>   Should all probabilities of insertion or deletion in the flow be combined together 
                              Default value: false. Possible values: {true, false} 

--flow-matrix-mods <String>   Modifications instructions to the read flow matrix. Format is src,dst{,src,dst}+. Example:
                              10,12,11,12 - these instructions will copy element 10 into 11 and 12  Default value: null.

--flow-mode <FlowMode>        Single argument for enabling the bulk of Flow Based features. NOTE: THIS WILL OVERWRITE
                              PROVIDED ARGUMENT CHECK TOOL INFO TO SEE WHICH ARGUMENTS ARE SET).  Default value: NONE.
                              Possible values: {NONE, STANDARD, ADVANCED} 

--flow-probability-scaling-factor <Integer>
                              probability scaling factor for (phred=10) for probability quantization  Default value: 10.

--flow-probability-threshold <Double>
                              Lowest probability ratio to be used as an option  Default value: 0.003. 

--flow-quantization-bins <Integer>
                              Number of bins for probability quantization  Default value: 121. 

--flow-remove-non-single-base-pair-indels <Boolean>
                              Should the probabilities of more then 1 indel be used  Default value: false. Possible
                              values: {true, false} 

--flow-remove-one-zero-probs <Boolean>
                              Remove probabilities of basecall of zero from non-zero genome  Default value: false.
                              Possible values: {true, false} 

--flow-report-insertion-or-deletion <Boolean>
                              Report either insertion or deletion, probability, not both  Default value: false. Possible
                              values: {true, false} 

--flow-retain-max-n-probs-base-format <Boolean>
                              Keep only hmer/2 probabilities (like in base format)  Default value: false. Possible
                              values: {true, false} 

--flow-symmetric-indel-probs <Boolean>
                              Should indel probabilities be symmetric in flow  Default value: false. Possible values:
                              {true, false} 

--flow-use-t0-tag <Boolean>   Use t0 tag if exists in the read to create flow matrix  Default value: false. Possible
                              values: {true, false} 

--force-active <Boolean>      If provided, all regions will be marked as active  Default value: false. Possible values:
                              {true, false} 

--force-call-filtered-alleles,-genotype-filtered-alleles <Boolean>
                              Force-call filtered alleles included in the resource specified by --alleles  Default
                              value: false. Possible values: {true, false} 

--gvcf-lod-band,-LODB <Double>Exclusive upper bounds for reference confidence LOD bands (must be specified in increasing
                              order)  This argument may be specified 0 or more times. Default value: [-2.5, -2.0, -1.5,
                              -1.0, -0.5, 0.0, 0.5, 1.0]. 

--independent-mates <Boolean> Allow paired reads to independently support different haplotypes.  Useful for validations
                              with ill-designed synthetic data.  Default value: false. Possible values: {true, false} 

--keep-boundary-flows <Boolean>
                              prevent spreading of boundary flows.  Default value: false. Possible values: {true, false}

--kmer-size <Integer>         Kmer size to use in the read threading assembler  This argument may be specified 0 or more
                              times. Default value: [10, 25]. 

--likelihood-calculation-engine <Implementation>
                              What likelihood calculation engine to use to calculate the relative likelihood of reads vs
                              haplotypes  Default value: PairHMM. Possible values: {PairHMM, FlowBased, FlowBasedHMM} 

--linked-de-bruijn-graph <Boolean>
                              If enabled, the Assembly Engine will construct a Linked De Bruijn graph to recover better
                              haplotypes  Default value: false. Possible values: {true, false} 

--max-mnp-distance,-mnp-dist <Integer>
                              Two or more phased substitutions separated by this distance or less are merged into MNPs. 
                              Default value: 1. 

--max-num-haplotypes-in-population <Integer>
                              Maximum number of haplotypes to consider for your population  Default value: 128. 

--max-prob-propagation-distance <Integer>
                              Upper limit on how many bases away probability mass can be moved around when calculating
                              the boundaries between active and inactive assembly regions  Default value: 50. 

--max-suspicious-reads-per-alignment-start <Integer>
                              Maximum number of suspicious reads (mediocre mapping quality or too many substitutions)
                              allowed in a downsampling stride.  Set to 0 to disable.  Default value: 0. 

--max-unpruned-variants <Integer>
                              Maximum number of variants in graph the adaptive pruner will allow  Default value: 100. 

--min-dangling-branch-length <Integer>
                              Minimum length of a dangling branch to attempt recovery  Default value: 4. 

--min-pruning <Integer>       Minimum support to not prune paths in the graph  Default value: 2. 

--minimum-allele-fraction,-min-AF <Double>
                              Lower bound of variant allele fractions to consider when calculating variant LOD  Default
                              value: 0.0. 

--num-pruning-samples <Integer>
                              Number of samples that must pass the minPruning threshold  Default value: 1. 

--pair-hmm-gap-continuation-penalty <Integer>
                              Flat gap continuation penalty for use in the Pair HMM  Default value: 10. 

--pair-hmm-implementation,-pairHMM <Implementation>
                              The PairHMM implementation to use for genotype likelihood calculations  Default value:
                              FASTEST_AVAILABLE. Possible values: {EXACT, ORIGINAL, LOGLESS_CACHING,
                              AVX_LOGLESS_CACHING, AVX_LOGLESS_CACHING_OMP, FASTEST_AVAILABLE} 

--pair-hmm-results-file <GATKPath>
                              File to write exact pairHMM inputs/outputs to for debugging purposes  Default value: null.

--pcr-indel-model <PCRErrorModel>
                              The PCR indel model to use  Default value: CONSERVATIVE. Possible values: {NONE, HOSTILE,
                              AGGRESSIVE, CONSERVATIVE} 

--phred-scaled-global-read-mismapping-rate <Integer>
                              The global assumed mismapping rate for reads  Default value: 45. 

--pileup-detection <Boolean>  If enabled, the variant caller will create pileup-based haplotypes in addition to the
                              assembly-based haplotype generation.  Default value: false. Possible values: {true, false}

--pruning-lod-threshold <Double>
                              Ln likelihood ratio threshold for adaptive pruning algorithm  Default value:
                              2.302585092994046. 

--pruning-seeding-lod-threshold <Double>
                              Ln likelihood ratio threshold for seeding subgraph of good variation in adaptive pruning
                              algorithm  Default value: 9.210340371976184. 

--recover-all-dangling-branches <Boolean>
                              Recover all dangling branches  Default value: false. Possible values: {true, false} 

--reference-model-deletion-quality <Byte>
                              The quality of deletion in the reference model  Default value: 30. 

--showHidden <Boolean>        display hidden arguments  Default value: false. Possible values: {true, false} 

--smith-waterman <Implementation>
                              Which Smith-Waterman implementation to use, generally FASTEST_AVAILABLE is the right
                              choice  Default value: FASTEST_AVAILABLE. Possible values: {FASTEST_AVAILABLE,
                              AVX_ENABLED, JAVA} 

--smith-waterman-dangling-end-gap-extend-penalty <Integer>
                              Smith-Waterman gap-extend penalty for dangling-end recovery.  Default value: -6. 

--smith-waterman-dangling-end-gap-open-penalty <Integer>
                              Smith-Waterman gap-open penalty for dangling-end recovery.  Default value: -110. 

--smith-waterman-dangling-end-match-value <Integer>
                              Smith-Waterman match value for dangling-end recovery.  Default value: 25. 

--smith-waterman-dangling-end-mismatch-penalty <Integer>
                              Smith-Waterman mismatch penalty for dangling-end recovery.  Default value: -50. 

--smith-waterman-haplotype-to-reference-gap-extend-penalty <Integer>
                              Smith-Waterman gap-extend penalty for haplotype-to-reference alignment.  Default value:
                              -11. 

--smith-waterman-haplotype-to-reference-gap-open-penalty <Integer>
                              Smith-Waterman gap-open penalty for haplotype-to-reference alignment.  Default value:
                              -260. 

--smith-waterman-haplotype-to-reference-match-value <Integer>
                              Smith-Waterman match value for haplotype-to-reference alignment.  Default value: 200. 

--smith-waterman-haplotype-to-reference-mismatch-penalty <Integer>
                              Smith-Waterman mismatch penalty for haplotype-to-reference alignment.  Default value:
                              -150. 

--smith-waterman-read-to-haplotype-gap-extend-penalty <Integer>
                              Smith-Waterman gap-extend penalty for read-to-haplotype alignment.  Default value: -5. 

--smith-waterman-read-to-haplotype-gap-open-penalty <Integer>
                              Smith-Waterman gap-open penalty for read-to-haplotype alignment.  Default value: -30. 

--smith-waterman-read-to-haplotype-match-value <Integer>
                              Smith-Waterman match value for read-to-haplotype alignment.  Default value: 10. 

--smith-waterman-read-to-haplotype-mismatch-penalty <Integer>
                              Smith-Waterman mismatch penalty for read-to-haplotype alignment.  Default value: -15. 

--soft-clip-low-quality-ends <Boolean>
                              If enabled will preserve low-quality read ends as softclips (used for DRAGEN-GATK BQD
                              genotyper model)  Default value: false. Possible values: {true, false} 

--use-pdhmm-overlap-optimization <Boolean>
                              PDHMM: An optimization to PDHMM, if set this will skip running PDHMM haplotype
                              determination on reads that don't overlap (within a few bases) of the determined allele in
                              each haplotype. This substantially reduces the amount of read-haplotype comparisons at the
                              expense of ignoring read realignment mapping artifacts. (Requires '--use-pdhmm' argument) 
                              Default value: false. Possible values: {true, false} 

Conditional Arguments for annotation:

Valid only if "AllelePseudoDepth" is specified:
--dirichlet-keep-prior-in-count <Boolean>
                              By default we don't keep the prior use in the output counts ase it makes it easier to
                              interpretthis quantity as the number of supporting reads specially in low depth sites. We
                              this toggled the prior is included  Default value: false. Possible values: {true, false} 

--dirichlet-prior-pseudo-count <Double>
                              Pseudo-count used as prior for all alleles. The default is 1.0 resulting in a flat prior 
                              Default value: 1.0. 

--pseudo-count-weight-decay-rate <Double>
                              A what rate the weight of a read decreases base on its informativeness; e.g. 1.0 is linear
                              decay (default), 2.0 is for quadratic decay  Default value: 1.0. 

Valid only if "AssemblyComplexity" is specified:
--assembly-complexity-reference-mode <Boolean>
                              If enabled will treat the reference as the basis for assembly complexity as opposed to
                              estimated germline haplotypes  Default value: false. Possible values: {true, false} 

Valid only if "PossibleDeNovo" is specified:
--denovo-depth-threshold <Integer>
                              Minimum depth (DP) for all trio members to be considered for de novo calculation.  Default
                              value: 0. 

--denovo-parent-gq-threshold <Integer>
                              Minimum genotype quality for parents to be considered for de novo calculation (separate
                              from GQ thershold for full trio).  Default value: 20. 

Valid only if "RMSMappingQuality" is specified:
--allow-old-rms-mapping-quality-annotation-data <Boolean>
                              Override to allow old RMSMappingQuality annotated VCFs to function  Default value: false.
                              Possible values: {true, false} 

Conditional Arguments for readFilter:

Valid only if "AmbiguousBaseReadFilter" is specified:
--ambig-filter-bases <Integer>Threshold number of ambiguous bases. If null, uses threshold fraction; otherwise,
                              overrides threshold fraction.  Default value: null.  Cannot be used in conjunction with
                              argument(s) maxAmbiguousBaseFraction

--ambig-filter-frac <Double>  Threshold fraction of ambiguous bases  Default value: 0.05.  Cannot be used in conjunction
                              with argument(s) maxAmbiguousBases

Valid only if "ExcessiveEndClippedReadFilter" is specified:
--max-clipped-bases <Integer> Maximum number of clipped bases on either end of a given read  Default value: 1000. 

Valid only if "FlowBasedTPAttributeValidReadFilter" is specified:
--read-filter-max-hmer <Integer>
                              maxHmer to use for testing in the filter  Default value: 12. 

Valid only if "FragmentLengthReadFilter" is specified:
--max-fragment-length <Integer>
                              Maximum length of fragment (insert size)  Default value: 1000000. 

--min-fragment-length <Integer>
                              Minimum length of fragment (insert size)  Default value: 0. 

Valid only if "IntervalOverlapReadFilter" is specified:
--keep-intervals <String>     One or more genomic intervals to keep  This argument must be specified at least once.
                              Required. 

Valid only if "JexlExpressionReadTagValueFilter" is specified:
--read-filter-expression <String>
                              One or more JEXL expressions used to filter  This argument must be specified at least
                              once. Required. 

Valid only if "LibraryReadFilter" is specified:
--library <String>            Name of the library to keep  This argument must be specified at least once. Required. 

Valid only if "MappingQualityReadFilter" is specified:
--maximum-mapping-quality <Integer>
                              Maximum mapping quality to keep (inclusive)  Default value: null. 

--minimum-mapping-quality <Integer>
                              Minimum mapping quality to keep (inclusive)  Default value: 20. 

Valid only if "MateDistantReadFilter" is specified:
--mate-too-distant-length <Integer>
                              Minimum start location difference at which mapped mates are considered distant  Default
                              value: 1000. 

Valid only if "OverclippedReadFilter" is specified:
--dont-require-soft-clips-both-ends <Boolean>
                              Allow a read to be filtered out based on having only 1 soft-clipped block. By default,
                              both ends must have a soft-clipped block, setting this flag requires only 1 soft-clipped
                              block  Default value: false. Possible values: {true, false} 

--filter-too-short <Integer>  Minimum number of aligned bases  Default value: 30. 

Valid only if "PlatformReadFilter" is specified:
--platform-filter-name <String>
                              Platform attribute (PL) to match  This argument must be specified at least once. Required.

Valid only if "PlatformUnitReadFilter" is specified:
--black-listed-lanes <String> Platform unit (PU) to filter out  This argument must be specified at least once. Required.

Valid only if "ReadGroupBlackListReadFilter" is specified:
--read-group-black-list <String>
                              A read group filter expression in the form "attribute:value", where "attribute" is a two
                              character read group attribute such as "RG" or "PU".  This argument must be specified at
                              least once. Required. 

Valid only if "ReadGroupReadFilter" is specified:
--keep-read-group <String>    The name of the read group to keep  Required. 

Valid only if "ReadLengthReadFilter" is specified:
--max-read-length <Integer>   Keep only reads with length at most equal to the specified value  Default value:
                              2147483647. 

--min-read-length <Integer>   Keep only reads with length at least equal to the specified value  Default value: 30. 

Valid only if "ReadNameReadFilter" is specified:
--read-name <String>          Keep only reads with this read name  This argument must be specified at least once.
                              Required. 

Valid only if "ReadStrandFilter" is specified:
--keep-reverse-strand-only <Boolean>
                              Keep only reads on the reverse strand  Required. Possible values: {true, false} 

Valid only if "ReadTagValueFilter" is specified:
--read-filter-tag <String>    Look for this tag in read  Required. 

--read-filter-tag-comp <Float>Compare value in tag to this value  Default value: 0.0. 

--read-filter-tag-op <Operator>
                              Compare value in tag to value with this operator. If T is the value in the tag, OP is the
                              operation provided, and V is the value in read-filter-tag, then the read will pass the
                              filter iff T OP V is true.  Default value: EQUAL. Possible values: {LESS, LESS_OR_EQUAL,
                              GREATER, GREATER_OR_EQUAL, EQUAL, NOT_EQUAL} 

Valid only if "SampleReadFilter" is specified:
--sample <String>             The name of the sample(s) to keep, filtering out all others  This argument must be
                              specified at least once. Required. 

Valid only if "SoftClippedReadFilter" is specified:
--invert-soft-clip-ratio-filter <Boolean>
                              Inverts the results from this filter, causing all variants that would pass to fail and
                              visa-versa.  Default value: false. Possible values: {true, false} 

--soft-clipped-leading-trailing-ratio <Double>
                              Threshold ratio of soft clipped bases (leading / trailing the cigar string) to total bases
                              in read for read to be filtered.  Default value: null.  Cannot be used in conjunction with
                              argument(s) minimumSoftClippedRatio

--soft-clipped-ratio-threshold <Double>
                              Threshold ratio of soft clipped bases (anywhere in the cigar string) to total bases in
                              read for read to be filtered.  Default value: null.  Cannot be used in conjunction with
                              argument(s) minimumLeadingTrailingSoftClippedRatio
```

## Citation

Benjamin, D. et al. (2019) Calling somatic snvs and indels with Mutect2, bioRxiv. Available at: https://doi.org/10.1101/861054