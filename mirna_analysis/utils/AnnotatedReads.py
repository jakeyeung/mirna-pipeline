'''
Created on 2014-05-20

@author: jyeung

Handles annotated sam files as classes. Requires both the annotated sam file and its corresponding statistics.
Annotated sam file and statistics file should be generated from annotate_aligned_reads.py

This class is useful for calculating TPM because stats file contains library depth.
'''

import csv

class AnnotatedReads(object):
    '''
    A class representing Annotated Sam File
    '''

    def __init__(self, annotated_reads_file, stats_file=None):
        '''
        Constructor
        '''
        self.areadspath = annotated_reads_file
        self.statspath = stats_file
        if self.statspath is not None:
            self.total_reads, self.matched_reads, self.nonmatched_reads = self.get_stats()

    def get_stats(self):
        '''
        Get relevant library depth information.
        Specifically: total_reads, matched_reads, nonmatched_reads
        '''
        with open(self.statspath, 'rb') as statsfile:
            for statsrow in statsfile:
                '''
                Given row: "total_reads=14661573\n", return 14661573
                Save that number to relevant variables:
                    total_reads
                    matched_reads
                    nonmatched_reads
                '''
                if statsrow.startswith('total_reads'):
                    #remove newline at end of row, split by '='
                    #then get element after the equal sign
                    total_reads = float(statsrow.rstrip().split('=')[1])
                elif statsrow.startswith('matched_reads'):
                    matched_reads = float(statsrow.rstrip().split('=')[1])
                elif statsrow.startswith('nonmatched_reads'):
                    nonmatched_reads = float(statsrow.rstrip().split('=')[1])
        return total_reads, matched_reads, nonmatched_reads

    def __enter__(self, delim='\t', header=True):
        self.areadsfile = open(self.areadspath)
        self.reader = csv.reader(self.areadsfile, delimiter=delim)
        #read first row if there is a header
        if header:
            self.header = self.reader.next()
        else:
            self.header = 'No header'
        return self.reader, self.header

    def __exit__(self, type, value, tb):
        self.areadsfile.close()

