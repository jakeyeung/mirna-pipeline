#!/usr/bin/python
# encoding: utf-8
'''
Description: Filter differentially expressed elements by p-value and fold change

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

__all__ = []
__version__ = 0.1
__date__ = 'May 23 2014'
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
    parser.add_option("-i", "--in", dest="infile", help="set input path (output from calculate_diff_deseq.py, (pval adjusted by adjust_pvalues.R optional)) [default: %default]", metavar="FILE")
    parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
    parser.add_option("-f", "--fc_threshold", dest="fc_threshold", type="float", help="minimum log 2 fc threshold (abs val) to filter [default: %default]", metavar="FLOAT")
    parser.add_option("-p", "--pval_threshold", dest="pval_threshold", type="float", help="max pval threshold to filter. [default: %default]", metavar="FLOAT")
    parser.add_option("--pval_colname", dest="pval_colname", help="Colname containing pvalues. If using non-adj pval, may differ from default [default: %default]", metavar="STR")
    parser.add_option("--fc_colname", dest="fc_colname", help="Colname containing fc values [default: %default]", metavar="STR")
    # set defaults
    parser.set_defaults(outfile="./out.txt", infile="./in.txt", fc_threshold=1., pval_threshold=0.05, pval_colname="bh_adj_pval", fc_colname="avg_pairwise_log2_fc")

    # process options
    (opts, args) = parser.parse_args(argv)

    if opts.verbose > 0:
        print("verbosity level = %d" % opts.verbose)
    if opts.infile:
        print("infile = %s" % opts.infile)
    if opts.outfile:
        print("outfile = %s" % opts.outfile)

    # MAIN BODY #

    outfile = open(opts.outfile, 'wb')
    outwriter = csv.writer(outfile, delimiter='\t')

    #readfile
    with open(opts.infile, 'rb') as infile:
        reader = csv.reader(infile, delimiter='\t')
        header = reader.next()
        #write header to file
        outwriter.writerow(header)
        writecount = 0
        for row in reader:
            #expect rownames: "avg_pairwise_log2_fc" and "bh_adj_pval"
            fc = float(row[header.index(opts.fc_colname)])
            pval = float(row[header.index(opts.pval_colname)])
            if fc >= opts.fc_threshold and pval <= opts.pval_threshold:
                # passed filter, write to file
                outwriter.writerow(row)
                writecount += 1
    if opts.verbose > 0:
        print '%s rows written to file: %s' %(writecount, opts.outfile)
    outfile.close()



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
