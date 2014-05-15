#!/bin/sh
#bwn_aln_and_samse.sh
#Jake Yeung
#May 14 2014
#usage: bash bwn_aln_and_samse.sh
#requires $ref_fasta, $fastafile, $alnoutput, $samfile to be defined (e.g. -v option in qsub)

# Add path
export PATH=$PATH:/home/stas/Software/BWA/bwa-0.7.5a
#check output files do not exist as a safety.
if [[ -e $alnoutput ]] || [[ -e $samfile ]]
then
	echo "Warning: aln output: $alnoutput or sam output: $samfile exists, aborting run."
else	
	echo "Running alignment and converting to sam file..."	
	echo "Ref fasta: $ref_fasta"
	echo "Fasta input: $fastafile"
	echo "bwa aln output: $alnoutput"
	echo "samfile: $samfile"
	bwa aln -t 1 $ref_fasta $fastafile > $alnoutput
	bwa samse $ref_fasta $alnoutput $fastafile > $samfile
fi
