#!/bin/sh
#run_bwa.sh
#Jake Yeung
#May 14 2014
#Runs bwa on linuxsrv001, running this on cluster results in seg fault error
# Add path
export PATH=$PATH:/home/stas/Software/BWA/bwa-0.7.5a

sampdir=/home/collins/bgi_drives_all_smallRNA_seq
reffasta=/home/collins/databases/HG19_for_BWA/Homo_sapiens.GRCh37.62.dna.chromosome.fa
for samp in `ls -d $sampdir/CH*`
do
	#run BWA
	sampname=$(basename $samp)
	bwa aln -t 8 $reffasta $samp/$sampname.clean.fa > $samp/$sampname.bwa.sai
	bwa samse $reffasta $samp/$sampname.bwa.sai $samp/$sampname.clean.fa > $samp/$sampname.bwa.sam
done

