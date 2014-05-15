#!/bin/sh
#create_fa_files.sh
#Jake Yeung
#May 14 2014
#usage: bash create_fa_files.sh
#requires $sampout and $sampin to be defined (e.g. -v option in qsub)

#check $sampout does not exist as a safety.
if [[ -e $sampout ]]
then
	echo "Warning: output $sampout exists, aborting..."
else
	echo "Creating fasta file from input: $sampin"
	echo "Writing output to $sampout"
	#print fa header as ">Counter|number_of_reads($2)"
	#$3 is the sequence
	awk '{print ">" n++ "|" $2; print $3}' $sampin > $sampout
fi
