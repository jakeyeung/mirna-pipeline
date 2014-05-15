#!/bin/sh
# Jake Yeung
# May 12 2014
# fastq_qc.sh
# Run fastq QC scripts to check quality

# Function for running processes in parallel
run_parallel(){
	proc_count=1
	for d in `ls $mirnadir`;
	do
		echo "Running command $1"
		fastq=$mirnadir/$d/$d.fq
		qc_dirname=fastx_qc
		qc_outfile=$mirnadir/$d/$qc_dirname/$d.stats.txt
		eval $1
		if (( $proc_count % $max_procs  == 0 )); then wait; fi
		proc_count=`expr $proc_count + 1`
	done
	wait
}

# Set number of processes to launch in parallel
max_procs=10

mirnadir="/home/collins/bgi_drives_all_smallRNA_seq"

run_parallel 'fastx_quality_stats -i $fastq -o $qc_outfile&'
run_parallel 'fastq_quality_boxplot_graph.sh -i $qc_outfile -o $mirnadir/$d/$qc_dirname/"$d"_quality.png -t "$d"&'
run_parallel 'fastx_nucleotide_distribution_graph.sh -i $qc_outfile -o $mirnadir/$d/$qc_dirname/"$d"_nuc.png -t "$d"&'

#for d in `ls $mirnadir`;
#do
#	echo "Making stat QC file for sample $d"
#	fastq=$mirnadir/$d/$d.fq
#	# make stats folder
#	qc_dirname=fastx_qc
#	mkdir $mirnadir/$d/$qc_dirname
#	qc_outfile=$mirnadir/$d/$qc_dirname/$d.stats.txt
#	fastx_quality_stats -i $fastq -o $qc_outfile&
#	if (( $proc_count % $max_procs  == 0 )); then wait; fi
#	proc_count=`expr $proc_count + 1`
#done
#
#for d in `ls $mirnadir`;
#do
#    echo "Generating quality plots for $d"
#	fastq=$mirnadir/$d/$d.fq
#	qc_dirname=fastx_qc
#	qc_outfile=$mirnadir/$d/$qc_dirname/$d.stats.txt
#	fastq_quality_boxplot_graph.sh -i $qc_outfile -o $mirnadir/$d/$qc_dirname/"$d"_quality.png -t "$d"&
#	if (( $proc_count % $max_procs  == 0 )); then wait; fi
#	proc_count=`expr $proc_count + 1`
#done
#
#for d in `ls $mirnadir`;
#do
#    echo "Generating quality plots for $d"
#    fastq=$mirnadir/$d/$d.fq
#    qc_dirname=fastx_qc
#    qc_outfile=$mirnadir/$d/$qc_dirname/$d.stats.txt
#    fastq_quality_boxplot_graph.sh -i $qc_outfile -o $mirnadir/$d/$qc_dirname/"$d"_nuc.png -t "$d"&
#    if (( $proc_count % $max_procs  == 0 )); then wait; fi
#    proc_count=`expr $proc_count + 1`
#
#	#fastx_quality_stats -i $fastq -o $qc_outfile&
#	#fastq_quality_boxplot_graph.sh -i $qc_outfile -o $mirnadir/$d/$qc_dirname/"$d"_quality.png -t "$d"
#	#fastq_quality_boxplot_graph.sh -i $qc_outfile -o $mirnadir/$d/$qc_dirname/"$d"_nuc.png -t "$d"
#done

