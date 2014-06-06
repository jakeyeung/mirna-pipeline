# Jake Yeung
# 23 Aug 2013
# modified May 22 2014 to a more geneirc function

# ARgs --------------------------------------------------------------------


args <- commandArgs(trailingOnly=TRUE)
filename <- args[1]
output_filename <- args[2]


# Main --------------------------------------------------------------------

pval_summary <- read.table(filename, 
                           header=TRUE,
						   sep='\t')

pvals <- pval_summary$pval    # Second column.

pvals.adjusted <- p.adjust(pvals, method='BH')

# Create new dataframe with pvals.adjusted as new column
# place new column to right of unadjusted pvals.
output_df <- cbind(pval_summary, bh_adj_pval=pvals.adjusted)

# Save df to a new filename
write.table(output_df, file=output_filename, sep='\t', 
			row.names=TRUE, quote=FALSE, col.names=NA)
print(paste('Adjusted', length(pvals.adjusted), 'p-values.'))
print(paste('BH-adjusted file saved to', output_filename))
