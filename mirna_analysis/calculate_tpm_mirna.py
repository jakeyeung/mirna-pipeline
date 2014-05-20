#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Description:

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
__date__ = 'May 20 2014'
__updated__ = ''

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def calculate_tpm(reads, total_mapped_reads):
    '''
    Calculates tpm (transcripts per million mapped reads) in mirna samples.
    Concretely, since each read in mirna represents the entire mirna transcript, we can
    calculate TPM by:
        reads / million_mapped_reads
    '''
    million_mapped_reads = total_mapped_reads / 1000000.
    return float(reads) / million_mapped_reads

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
    parser.add_option("-i", "--in", dest="infile", help="set annotated reads file path [default: %default]", metavar="FILE")
    parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
    parser.add_option("-s", "--statsfile", dest="statsfile", help="set statistics path [default: %default]", metavar="FILE")
    # set defaults
    parser.set_defaults(outfile="./out.txt", infile="./in.txt", statsfile="./stats.txt")

    # process options
    (opts, args) = parser.parse_args(argv)

    if opts.verbose > 0:
        print("verbosity level = %d" % opts.verbose)
    if opts.infile:
        print("infile = %s" % opts.infile)
    if opts.statsfile:
        print("statsfile = %s" %opts.statsfile)
    if opts.outfile:
        print("outfile = %s" % opts.outfile)

    # MAIN BODY
    # init outfile
    tpm_outfile = open(opts.outfile, 'wb')
    tpm_writer = csv.writer(tpm_outfile, delimiter='\t')
    insert_index = -1    # insert TPM info at second last column of read row
    # read annotated reads, calculate TPM for each miRNA
    annotated_reads = AnnotatedReads.AnnotatedReads(opts.infile, opts.statsfile)
    with annotated_reads:
        # write output header by adding TPM to annotatedreads header
        annotated_reads.header.insert(insert_index, 'TPM')
        tpm_writer.writerow(annotated_reads.header)
        for rowcount, row in enumerate(annotated_reads.reader):
            reads = float(row[annotated_reads.header.index('reads')])
            annotated_reads.get_stats()
            tpm = calculate_tpm(reads, annotated_reads.total_reads)
            # write output row by adding TPM to annotatedreads row
            row.insert(insert_index, tpm)
            tpm_writer.writerow(row)
    if opts.verbose > 0:
        print '%s rows written to output.' %rowcount
    tpm_outfile.close()

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