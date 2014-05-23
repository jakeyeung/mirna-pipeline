# Jake Yeung
# May 22 2014
# deseq_normalization.R
# Creates normalized read counts using deseq package
# adapted from Fan Mo

library("DESeq")

options(echo=TRUE)
args <- commandArgs(trailingOnly=TRUE)

inputfile <- args[1]
outputfile <- args[2]

countTable_All <- read.table(file=inputfile, head=TRUE, row.names=1, sep="\t")

n_samples <- ncol(countTable_All)    # one column is microRNA id
print(n_samples)
conds <- factor(rep("NA", n_samples))

str(countTable_All)

cds_All <- newCountDataSet(countTable_All, conds)

cds_All <- estimateSizeFactors(cds_All)
cds_All <- estimateDispersions(cds_All)

normalizedCounts_All <- t(t(counts(cds_All)) / sizeFactors(cds_All))

write.table(normalizedCounts_All, file=outputfile, sep="\t", quote=FALSE, col.names=NA)

