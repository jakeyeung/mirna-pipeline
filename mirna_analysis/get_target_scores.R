# Jake Yeung
# May 23 2014
# get_target_scores.R
# use TargetScore and TargetScoreData packages to get miRNA-gene interactions

library(TargetScoreData)
targetScoreMatrix <- get_precomputed_targetScores()

args <- commandArgs(trailingOnly=TRUE)
mirna_name <- args[1]
outfile <- args[2]

print(paste("Trying to extract miRNA: ", mirna_name))
mirna_targetscores <- targetScoreMatrix[[which(names(targetScoreMatrix) == mirna_name)]]

write.table(mirna_targetscores, outfile, sep='\t', row.names=TRUE, col.names=NA, quote=FALSE)
print(paste(mirna_name, " target genes written to file: ", outfile))

