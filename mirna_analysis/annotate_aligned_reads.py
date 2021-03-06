#!/usr/bin/python
# encoding: utf-8
'''
Description: annotate_aligned_reads takes sam files (created from run_bwa.sh
or some other alignment workflow) and annotates gene information.

This script was written for miRNA in mind, so the method, get_n_reads_from_mirna_id
may not be applicable to other applications.

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

from optparse import OptionParser

import csv
from utils import Annotations, SamParser

__all__ = []
__version__ = 0.1
__date__ = '2014-05-16'
__updated__ = '2014-05-16'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def get_n_reads_from_mirna_id(mirna_sam_id):
    '''
    Given ID from sam file of miRNA, retrieve number of reads.
    eg: 0|1237170 <- example miRNA id
    Return 1237170
    '''
    return mirna_sam_id.split('|')[1]

def get_annotations(dickey, gff3_dic):
    '''
    Given key, try to get annotations from gff3_dic.
    If dickey not in gff3_dic, it will throw error...
    '''
    annot = gff3_dic[dickey]['attrib']    # miRNA annotation info
    return annot

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
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-i", "--in", dest="infile", help="set input path [default: %default]", metavar="FILE")
        parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
        parser.add_option("-a", "--annotfile", dest="annotfile", help="set annotation file path [default: %default]", metavar="FILE")
        parser.add_option("-f", "--force", dest="force", action="store_true", help="If output file exists already, overwrite it anyway.")
        parser.add_option("-m", "--max_offset", dest="max_offset", type="int", help="Adjust start positions up to a max offset in order to find unmatched reads. [default: %default]", metavar="INT")
        parser.add_option("-s", "--stats_outfile", dest="stats_outpath", help="Output file of statistics of matched and nonmatched reads [default: %default]", metavar="FILE")
        parser.add_option("-t", "--track_offset", dest="track_offset", action="store_true", help="Add offset value to ID to keep track of the offset, default is off")
        # set defaults
        parser.set_defaults(outfile="./out.txt", infile="./in.txt", annotfile="$HOME/data/mirna_annotations/hsa.gff3", max_offset=5, stats_outpath="./stats.txt")

        # process options
        (opts, args) = parser.parse_args(argv)

        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)
        if opts.infile:
            print("infile = %s" % opts.infile)
        if opts.outfile:
            print("outfile = %s" % opts.outfile)
        if opts.annotfile:
            print("annotfile = %s" % opts.annotfile)
        if opts.force:
            print("force = %s" % opts.force)
        if opts.max_offset:
            print("max_offset = %s" %opts.max_offset)
        if opts.stats_outpath:
            print("stats_outpath = %s" %opts.stats_outpath)
        if opts.track_offset:
            print("track_offset = %s" %opts.track_offset)
        # MAIN BODY #

        # index gff3 annotations
        gff3_annotations = Annotations.Gff3(gff3_filepath=opts.annotfile)
        gff3_dic = gff3_annotations.index()
        gff3_dickeys = gff3_annotations.get_dic_subkeys()
        if opts.verbose > 0:
            print('gff3 file (%s) annotated.\nIndexed dic contains %s entries.' %(opts.annotfile, len(gff3_dic.keys())))
            print('Example key: %s' %gff3_dic.keys()[0])

        # init output file
        if os.path.exists(opts.outfile):
            if opts.force:
                if opts.verbose > 0:
                    print('Overwriting existing outfile: %s. Disable --force if '\
                            'you dont want this to happen.' %opts.outfile)
            else:
                print("Outfile %s exists. \nAborting..." %opts.outfile)
                sys.exit()
        annotated_sam_outfile = open(opts.outfile, 'wb')
        outwriter = csv.writer(annotated_sam_outfile, delimiter='\t')
        # write header: chromo, start, end, strand, seq, accession_number
        header = ['chr', 'start', 'end', 'strand', 'reads', 'annotations']
        outwriter.writerow(header)

        # open sam file, get elements in each row of sam file
        sam_file = SamParser.SamFile(opts.infile)
        match_count = 0
        match_reads = 0
        nomatch_count = 0
        nomatch_reads = 0
        reads_total = 0
        with sam_file:
            for writecount, samrow in enumerate(sam_file):
                dickey = '%s:%s:%s' %(samrow.chromo, samrow.start, samrow.strand)
                # match dickey to dic
                reads = int(get_n_reads_from_mirna_id(samrow.id))
                reads_total += reads
                if dickey in gff3_dic:
                    annot = gff3_dic[dickey]['attrib']    # miRNA annotation info
                    match_count += 1
                    match_reads += reads
                else:
                    '''
                    # not in dic. First try harder. Could be off by one or two
                    # reads. We'll count +/- 10
                    First change dickey start to start+1, check if it's in dic. Then
                    do dickey start to start-1, check if it's dic.
                    Repeat until some increment, say +/-10 or some maximum defined
                    by options (user-settable)
                    '''
                    #----Begin trying +/- starts to get match to annotations...
                    offset = 1
                    matched = False
                    while (matched==False) and (offset <= opts.max_offset):
                        dickey_pos_offset = '%s:%s:%s' %(samrow.chromo,
                                                        (samrow.start+offset),
                                                        samrow.strand)
                        dickey_neg_offset = '%s:%s:%s' %(samrow.chromo,
                                                        (samrow.start-offset),
                                                        samrow.strand)
                        if dickey_pos_offset in gff3_dic:
                            annot = gff3_dic[dickey_pos_offset]['attrib']
                            #add offset information into annot if option set
                            if opts.track_offset:
                                annot = '%s;Offset=%s' %(annot, offset)
                            match_count += 1
                            match_reads += reads
                            matched = True
                        elif dickey_neg_offset in gff3_dic:
                            annot = gff3_dic[dickey_neg_offset]['attrib']
                            #add offset information into annot if option set
                            if opts.track_offset:
                                annot = '%s;Offset=%s' %(annot, (-1*offset))
                            match_count += 1
                            match_reads += reads
                            matched = True
                        else:
                            # neither pos or neg increment worked, try
                            # increasing offset and repeat.
                            offset += 1
                    #----End trying +/- starts to get match to annotations...
                    if matched is False:
                        annot = samrow.flag
                        nomatch_count += 1
                        nomatch_reads += reads
                header = \
                    [samrow.chromo, samrow.start, samrow.end, samrow.strand, reads, annot]
                outwriter.writerow(header)
        annotated_sam_outfile.close()

        frac_reads_mapped = float(match_reads) / reads_total
        frac_reads_unmapped = float(nomatch_reads) / reads_total
        if opts.verbose > 0:
            print('%s rows written to: %s' %(writecount, opts.outfile))
            print('%s matched to gff3 file. %s not matched to gff3 file.' \
                  %(match_count, nomatch_count))
            print('Statistics:\n%s/%s (%s) reads mapped.\n%s/%s (%s) reads unmapped.' \
                  %(match_reads, reads_total, frac_reads_mapped,
                    nomatch_reads, reads_total, frac_reads_unmapped))

        #write a statistics file output
        with open(opts.stats_outpath, 'wb') as stats_outfile:
            total_reads_row = 'total_reads=%s\n' %reads_total
            match_reads_row = 'matched_reads=%s\n' %match_reads
            nomatch_reads_row = 'nonmatched_reads=%s\n' %nomatch_reads
            frac_reads_mapped_row = 'frac_matched_reads=%s\n' %frac_reads_mapped
            frac_reads_unmapped_row = 'frac_nonmatched_reads=%s\n' %frac_reads_unmapped
            for row in [total_reads_row, match_reads_row, nomatch_reads_row,
                        frac_reads_mapped_row, frac_reads_unmapped_row]:
                stats_outfile.write(row)
            if opts.verbose > 0:
                print('Statistics file written to: %s' %opts.stats_outpath)

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2


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
