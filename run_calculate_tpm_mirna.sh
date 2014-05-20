#!/bin/bash
# Jake Yeung
# May 20 2014
# Jake Yeung
# Run calculate_tpm_mirna.py on cluster

mirna_dir=/home/collins/bgi_drives_all_smallRNA_seq
calc_tpm_script=/home/jyeung/scripts/submission_scripts/calculate_tpm.sh
qsub_outdir=/home/jyeung/scripts/qsub_out

for samp in `ls $mirna_dir`
do
	#----Calculates tpm from annotated mirna file
	echo "Input file: $mirna_dir/$samp/$samp.annotated"
	echo "Output file: $mirna_dir/$samp/$samp.annotated.tpm"
	echo "Mapping statistics file: $mirna_dir/$samp/$samp.annotated.stats"
	qsub -S /bin/sh -N calc_tpm_mirna -l h_vmem=500M,virtual_free=100M -notify -b y -j y -o $qsub_outdir/"$samp"_calc_tmp.out -e $qsub_outdir/"$samp"_calc_tmp.err -v annotated_file=$mirna_dir/$samp/$samp.annotated,annotated_with_tpm_outfile=$mirna_dir/$samp/$samp.annotated.tpm,statsfile=$mirna_dir/$samp/$samp.annotated.stats $calc_tpm_script
done
