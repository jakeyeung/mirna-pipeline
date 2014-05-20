#!/bin/sh
# annotate_reads.sh
# Jake Yeung
# May 20 2014
# Runs python script: annotate_aligned_reads.py
# variables $samfile and $outfile are defined when running qsub script

align_reads_pyscript="mirna_analysis/annotate_aligned_reads.py"
annotfile="/home/jyeung/data/mirna_annotations/hsa.gff3"

python $align_reads_pyscript -v -f -i $samfile -a $annotfile -o $outfile
