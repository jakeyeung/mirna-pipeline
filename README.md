# miRNA pipeline
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
* [Get target score information for a given miRNA](#targetscore)
* [Plot expression differences between an miRNA and protein-coding gene](#plotexprs)

<a name="uncompress"/>
## Processing of miRNA data

### Basic ideas for what `uncompress_and_align_mirna.sh` does:
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

<a name "targetscore"/>
## Get target score information for a given miRNA.
Required packages: `TargetScoreData`

### Procedure
`Rscript get_target_scores.R mirna_name outfile`

### Example:
`Rscript get_target_scores.R hsa-miR-517a hsa-miR-517a.targetscores

### Notes:
* Only a subset of miRNAs have available target scores (likely because they have yet to do the siRNA knockdown experiment).
* To get the list of available miRNAs:
```
library(TargetScoreData)
targetScoreMatrix <- get_precomputed_targetScores()
names(targetScoreMatrix)
```

<a name="plotexprs"/>
## Plot expression differences between an miRNA and protein-coding gene

### Procedure for `mirna_analysis/plot_exprs_diff.py`:

To plot expression differences for a single gene:
* `python mirna_analysis/plot_exprs_diff.py -i /exprs/of/gene/across/samples.txt -g gene_of_interest -c 'Gene ID column name' -s /pairs/of/samples.txt`

To plot expression differences for a two genes (to compare expression of miRNA and a gene of interest, for example):
* Second gene may be from a different file (e.g., you may process miRNA and protein-coding genes separately and therefore have two separate files for them)
* If so, specify the additional textfile as so:
`python mirna_analysis/plot_exprs_diff.py -i exprs_file1 -I exprs_file2 -g gene1 -G gene2 -c 'gene_colname1' -C 'gene_colname2' -s /pairs/of/samples.txt`

Notes:
* Expression file should contain a column containing gene IDs, with a column name that is specified using `-c`.
* Expression file should contain expression across samples. The script identifies pairs of samples (e.g. tumour and adjacent benign) through the sample pairs textfile provided by `-s`.

