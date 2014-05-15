#!/bin/bash
#mirna_pipeline.sh
#Jake Yeung
#May 9 2014
#Pipline for processing mirna data

#Permissions had to be changed by logging to mofan
#chmod g+wr */*

# Set mirna dir
mirna_dir=/home/collins/bgi_drives_all_smallRNA_seq
submission_bash_script=/home/jyeung/scripts/submission_scripts/zcat_sample.sh
create_fa_script=/home/jyeung/scripts/submission_scripts/create_fa_files.sh
run_bwa_script=/home/jyeung/scripts/submission_scripts/bwa_aln_and_samse.sh
qsub_outdir=/home/jyeung/scripts/qsub_out
for samp in `ls $mirna_dir`
do
	#----------zcat for uncompressing .fq.gz to .fq
	qsub -S /bin/sh -N zcat_samps -l h_vmem=500M,virtual_free=100M -notify -b y -j y -o $qsub_outdir/"$samp"_zcat.out -e $qsub_outdir/"$samp"_zcat.err -v sampin=$mirna_dir/$samp/$samp.fq.gz,sampout=$mirna_dir/$samp/$samp.zcat.fq $submission_bash_sicript
	#----------uncompress clean.txt.gz files to clean.zcat.txt
	cleaninput=$mirna_dir/$samp/clean.txt.gz
	cleanoutput=$mirna_dir/$samp/clean.txt
	qsub -S /bin/sh -N zcat_samps -l h_vmem=500M,virtual_free=100M -notify -b y -j y -o $qsub_outdir/"$samp"_zcat.test.clean.out -e $qsub_outdir/"$samp"_zcat.test.clean.err -v sampin=$mirna_dir/$samp/$cleaninput,sampout=$mirna_dir/$samp/$cleanoutput $submission_bash_script
	#----------Create fasta file from clean.zcat.txt
	fastainput=$cleanoutput
	fasta=$mirna_dir/$samp/$samp.clean.fa
	qsub -S /bin/sh -N create_fa_files -l h_vmem=500M,virtual_free=100M -notify -b y -j y -o $qsub_outdir/"$samp".fa.out -e $qsub_outdir/"$samp"_fa.err -v sampin=$mirna_dir/$samp/$fastainput,sampout=$mirna_dir/$samp/$fasta $create_fa_script
	#----------Run BWA alignment
	#default parameters to start
	#ref_fasta=/home/collins/databases/HG19_for_BWA/Homo_sapiens.GRCh37.62.dna.chromosome.fa #causes segmentation fault because this file is indexed with different version from xavier2
	ref_fasta=/home/collins/databases/for_BWA/hg19_plus_mm10/hg19_plus_mm10.fa
	sam_output=$mirna_dir/$samp/$samp.sam
	alnoutput=$mirna_dir/$samp/$samp.sai
	#align to reference
	qsub -S /bin/sh -N bwn_aln_samse -l h_vmem=15G,virtual_free=13G -notify -b y -j y -o $qsub_outdir/"$samp".bwa.out -e $qsub_outdir/"$samp".bwa.err -v ref_fasta=$ref_fasta,fastafile=$fasta,alnoutput=$alnoutput,samfile=$sam_output $run_bwa_script
	#takes about 30 minutes on the cluster.
done
