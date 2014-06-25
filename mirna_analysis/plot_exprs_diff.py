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
import math
from optparse import OptionParser
from plot_utils import jplots

__all__ = []
__version__ = 0.1
__date__ = 'June 25 2014'
__updated__ = ''

DEBUG = 0
TESTRUN = 0
PROFILE = 0


def get_sample_pairs(sample_pairs_file):
    '''
    Read filename containing sample pairs.
    Expected file format:
        column 1: samples in group 1
        column 2: samples in group 2
    Output a list of tuples. Each tuple contains paired sample
    from group 1 and 2.
    '''
    sample_pairs = []
    with open(sample_pairs_file, 'rb') as readfile:
        jreader = csv.reader(readfile, delimiter='\t')
        for row in jreader:
            sample_group1 = row[0]
            sample_group2 = row[1]
            if all([sample_group1 != '', sample_group2 != '']):
                sample_pairs.append((row[0], row[1]))
    return sample_pairs


def get_paired_exprs_diffs(infile, sample_pairs, genename=None, convert_to_log2=True):
    '''
    Read file, find gene name. Get expression values for each sample_pair,
    return a list of differences in gene expression between paired samples.

    Expect first row to contain gene name.
    '''
    exprs_diffs = []
    with open(infile, 'rb') as readfile:
        jreader = csv.reader(readfile, delimiter='\t')
        header = jreader.next()
        for row in jreader:
            if row[0] != genename:
                continue
            else:
                for sample_pair in sample_pairs:
                    exprs1 = float(row[header.index(sample_pair[0])])
                    exprs2 = float(row[header.index(sample_pair[1])])
                    if convert_to_log2:
                        exprs1 = math.log(exprs1, 2)
                        exprs2 = math.log(exprs2, 2)
                    exprs_diff = exprs2 - exprs1
                    exprs_diffs.append(exprs_diff)
    return exprs_diffs


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
    parser.add_option("-i", "--in", dest="infile", help="set input path [default: %default]", metavar="FILE")
    parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
    parser.add_option("-g", "--genename", dest="genename", metavar="GENENAME", help="First gene name to plot expression")
    parser.add_option("-c", "--gene_colname", dest="gene_colname", metavar="COLUMNNAME", help="Column name containing gene name [default: %default]")
    parser.add_option("-s", "--samplepairsfile", dest="samplepairsfile", metavar="FILE", help="File name containing sample pairs. Column 1 and 2 contains samples from group 1 and 2, respectively.")

    # set defaults
    parser.set_defaults(outfile="./out.txt", infile="./in.txt", gene_colname='')

    # process options
    (opts, args) = parser.parse_args(argv)

    if opts.verbose > 0:
        print("verbosity level = %d" % opts.verbose)
    if opts.infile:
        print("infile = %s" % opts.infile)
    if opts.outfile:
        print("outfile = %s" % opts.outfile)
    if opts.samplepairsfile:
        print("samplepairsfile = %s" % opts.samplepairsfile)
    if opts.genename:
        print("genename = %s" % opts.genename)

    # MAIN BODY #
    sample_pairs = get_sample_pairs(opts.samplepairsfile)

    exprs_diff = get_paired_exprs_diffs(opts.infile, sample_pairs, genename=opts.genename)

    jplots.plot_vertical_scatter(exprs_diff,
                                 jitter=True,
                                 title='Paired differences of tumours: %s' % opts.genename,
                                 xlabel=opts.genename,
                                 ylabel='Fold Change Difference (log2)')


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