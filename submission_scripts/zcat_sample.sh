#!/bin/sh
#zcat_samples.sh
#Jake Yeung
#May 12 2014
#define beforehand: $sampin $sampout in qsub script
#usage: bash zcat_samples.sh
#Outputs zcats $sampin, outputs $sampout

# if $sampout already exists, or $sampin does not exist, do not
# zcat, this is a safety precaution. I lost data when $sampout existed
# and $sampin did not exist, making me overwrite an empty file to $sampout.
if [[ -e $sampout ]] || [[ ! -e $sampin ]]
then
	echo "Warning: output $sampout exists or input $sampin does not exist, aborting overwrite..."
else
	echo "$sampout is safe to write. Running zcat..."
	echo "zcat $sampin > $sampout"
fi
