#!/bin/bash
# Jake Yeung
# May 20 2014
# Jake Yeung
# run_annotate_aligned_reads.sh
# Runs python script annotate_aligned_reads.sh

mirna_dir=/home/collins/bgi_drives_all_smallRNA_seq
annotate_reads_script=/home/jyeung/scripts/submission_scripts/annotate_reads.sh
qsub_outdir=/home/jyeung/scripts/qsub_out
for samp in `ls $mirna_dir`
do
	#----Annotate aligned reads
	#echo "qsub outs: $qsub_outdir/'$samp'_annotate_aligned_reads.out"
	#echo "samfile=$mirna_dir/$samp/$samp.bwa.sam"
	#echo "outfile=$mirna_dir/$samp/$samp.annotated"
	#echo "shellscript=$annotate_reads_script"
	ls -l $mirna_dir/$samp/$samp.bwa.sam
	#qsub -S /bin/sh -N annotate_mirna_reads -l h_vmem=500M, virtual_free=100M -notify -b y -j y -o $qsub_outdir/"$samp"_annotate_aligned_reads.out -e $qsub_outdir/"$samp"_annotate_aligned_reads.err -v samfile=$mirna_dir/$samp/$samp.bwa.sam,outfile=$mirna_dir/$samp/$samp.annotated $annotate_reads_script
done
ls -l $annotate_reads_script
