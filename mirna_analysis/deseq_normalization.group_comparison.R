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
ttestoutputfile <- args[3]
ignore_first_n_cols <- args[4]
ignore_first_n_cols <- as.numeric(ignore_first_n_cols)

countTable_All <- read.table(file=inputfile, head=TRUE, sep="\t")

# Get subset containing only counts data
countTable_All.subset <- countTable_All[, -(1:ignore_first_n_cols)]

n_samples <- ncol(countTable_All.subset)    # one column is microRNA id
print(n_samples)
myfactors <- rep(c("N", "T"), floor(n_samples/2))
myfactors <- append(myfactors, "T")
conds <- factor(myfactors)

str(countTable_All.subset)

cds_All <- newCountDataSet(countTable_All.subset, conds)

cds_All <- estimateSizeFactors(cds_All)
cds_All <- estimateDispersions(cds_All)
res_All <- nbinomTest(cds_All, "T", "N")

write.table(res_All, file=ttestoutputfile, sep="\t", quote=FALSE, row.names=FALSE)

normalizedCounts_All <- t(t(counts(cds_All)) / sizeFactors(cds_All))

# Append normalizedCounts_All back to countTable_All
countTable_All <- cbind(countTable_All[, (1:ignore_first_n_cols)], normalizedCounts_All)

write.table(countTable_All, file=outputfile, sep="\t", quote=FALSE, row.names=FALSE)

