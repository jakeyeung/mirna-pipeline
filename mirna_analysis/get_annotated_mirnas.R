# Jake Yeung
# May 23 2014
# get_annotated_mirnas.R
# get mirnas with targetscore information

library(TargetScoreData)

args <- commandArgs(trailingOnly=TRUE)
outfile <- args[1]

targetScoreMatrix <- get_precomputed_targetScores()

mirna_ids <- data.frame('mirna'=sort(names(targetScoreMatrix)))

write.table(mirna_ids, outfile, quote=FALSE, row.names=FALSE)
