#!/bin/sh
# Jake Yeung 
# calculate_tpm.sh
# May 20 2014
# script that qsub calls to run tpm calculations

 pythonscript="/home/jyeung/scripts/mirna_analysis/calculate_tpm_mirna.py"

 python $pythonscript -v -i $annotated_file -o $annotated_with_tpm_outfile -s $statsfile

