# miRNA pipeline
## Jake Yeung
### June 6 2014

This is a repository containing scripts used to process miRNA data. 

Directory `mirna_analysis` contains python and R scripts used for processing miRNA.
These scripts should be somewhat general and can be used for other miRNA datasets or 
even gene expression data sets.

Main directory contains `qsub` scripts I wrote to run scripts in `mirna_analysis` (or
just programs such as bwa.

`submission_scripts` directory contains executable scripts that qsub can call. 

# Example Workflows
* [Uncompressing and aligning miRNA data](#uncompress)
* [BWA workflow](#bwa)
* [DESeq workflow](#deseq)

<a name="uncompress"/>
## Processing of miRNA data

### Procedure for `uncompress_and_align_mirna.sh`:
1. Uncompress `fq` files
2. Uncompress `clean.txt.gz` files
3. Create `fa` files
4. Run BWA

<a name="bwa"/>
## Running BWA
BWA can also be run separately (useful if you want to run on a local server rather than a cluster).

For example bash script: see `run_bwa.sh`

## Calculate TPM (transcripts per million mapped reads)

### Procedure for `calculate_tpm_mirna.py`:
1. Calculate TPM for aligned miRNA reads

For example bash script: see `run_calculate_tpm_mirna.sh` that calls the python script.

## Annotate SAM files (output from BWA) and annotate gene information.

`python mirna_analysis/annotate_aligned_reads.py --help` for more information regarding the script that annotates SAM files with gene information.

Example bash script: `run_annotate_aligned_reads.sh`

<a name="deseq"/>
## DESeq workflow

### Procedure:
1. Merge count data for samples using `mirna_analysis/merge_counts_data_for_deseq.py`
2. Run `mirna_analysis/deseq_normalization.R` from merged count data

