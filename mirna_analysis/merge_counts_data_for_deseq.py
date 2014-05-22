#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Description: merge counts data across many samples to create a
merged counts table suitable for DESeq analysis.
Takes as input a file containing a list of filepaths of annotated
read counts, creates a merged table of read counts by reading each path
in list of filepaths.


Classes and methods:

@author:     jakeyeung

@lab:  2014 Laboratory for Advanced Genome Analysis.

@license:    Apache License 2.0

@contact:    jakeyeung@gmail
        :    github.com/jakeyeung
@deffield    updated: None yet
'''

import sys
import os
import csv

from optparse import OptionParser

from utils import AnnotatedReads

__all__ = []
__version__ = 0.1
__date__ = 'May 22 2014'
__updated__ = ''

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2014 Jake Yeung (Laboratory for Advanced Genome Analysis)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]

    # setup option parser
    parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
    parser.add_option("-i", "--in", dest="infile", help="set input path containing list of filepaths [default: %default]", metavar="FILE")
    parser.add_option("-o", "--out", dest="outfile", help="set output path for merged read counts table[default: %default]", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
    parser.add_option("-n", "--nan", dest="nan", type="int", help="Output nan if sample does not have info on an miRNA.", metavar="INT")
    # set defaults
    parser.set_defaults(outfile="./out.txt", infile="./in.txt", nan=0)

    # process options
    (opts, args) = parser.parse_args(argv)

    if opts.verbose > 0:
        print("verbosity level = %d" % opts.verbose)
    if opts.infile:
        print("infile = %s" % opts.infile)
    if opts.outfile:
        print("outfile = %s" % opts.outfile)

    # MAIN BODY #
    # get list of files
    filepaths = []
    sampids = []
    with open(opts.infile, 'rb') as infile:
        infile_reader = csv.reader(infile, delimiter='\t')
        for row in infile_reader:
            # each row is a file path
            filepaths.append(row[0])
            sampids.append(row[1])

    merged_dic = {}
    for readsfile, sampid in zip(filepaths, sampids):
        readsobj = AnnotatedReads.AnnotatedReads(readsfile, stats_file=None)
        reads_dic = AnnotatedReads.index_annotatedreads_file(readsobj, count_id='reads', subdic=False)
        for annot_count, annot in enumerate(reads_dic):
            if annot not in merged_dic:
                # init subdic
                merged_dic[annot] = {}
            merged_dic[annot].update({sampid: reads_dic[annot]})
        if opts.verbose > 0:
            print('Sample: %s added to merged_dic (%s mirna IDs)' %(sampid, annot_count))

    #write to file
    with open(opts.outfile, 'wb') as outfile:
        outwriter = csv.writer(outfile, delimiter='\t')
        #write header: mirna ID + samples
        writeheader = ['id'] + sampids
        outwriter.writerow(writeheader)
        #write data: mirna ID + reads from samples
        writerowcount = 0
        for annot in merged_dic:
            writerow = [annot]    # append from mirnaID
            for sampid in sampids:
                #if sample has reads for miRNA: append that value
                #otherwise, write nan
                if sampid in merged_dic[annot]:
                    writerow.append(merged_dic[annot][sampid])
                else:
                    writerow.append(opts.nan)
            outwriter.writerow(writerow)
            writerowcount += 1
    if opts.verbose > 0:
        print '%s rows written to file: %s' %(writerowcount, opts.outfile)

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())