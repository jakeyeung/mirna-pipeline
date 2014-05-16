'''
Created on 2014-05-16

@author: jyeung
'''

import csv

class SamFile(object):
    '''
    A class representing a Sam File
    '''

    def __init__(self, sampath):
        '''
        Constructor
        '''
        self.path = sampath

    def __enter__(self, delim='\t'):
        self.file = open(self.path)
        self.reader = csv.reader(self.file, delimiter=delim)
        return self.reader

    def __exit__(self, type, value, tb):
        self.file.close()

    def __iter__(self):
        return self

    def next(self):
        #ignore rows beginning with '@'
        readrow = self.reader.next()
        while readrow[0].startswith('@'):
            readrow = self.reader.next()
        # our readrow does not begin with '@',
        # turn it into a SamRow object.
        return SamRow(readrow)

class SamRow(object):
    '''
    A class representing a ROW in a sam file
    '''


    def __init__(self, samrow, add_chr=True):
        '''
        See http://genome.sph.umich.edu/wiki/SAM for SAM file format
        We're interested in (by default)
        id (i=0), flag (i=1), chromo (i=2), start (i=3) and seq (i=9)

        add_chr: adds 'chr' to chromo (e.g, concatenates "chr" with "16" -> chr16)

        If sam file already is chr16, set add_chr=False
        '''
        self.row = samrow
        self.id = samrow[0]
        self.flag = int(samrow[1])
        #if flag is 16, strand is negative.
        #if flag is 0, strand is positive.
        #if flag is 4, strand is unmapped.
        if self.flag == 16:
            self.strand = '-'
        elif self.flag == 0:
            self.strand = '+'
        else:
            self.strand = None
        if add_chr:
            # add chr prefix
            self.chromo = '%s%s' %('chr', samrow[2])
        else:
            self.chromo = samrow[2]
        self.start = int(samrow[3])
        self.seq = samrow[9]
        #TODO: sanity check that this is correct on UCSC
        self.end = self.start + len(self.seq)

