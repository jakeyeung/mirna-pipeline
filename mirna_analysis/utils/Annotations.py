'''
Created on 2014-05-16

@author: jyeung

Handles annotation files as classes.
'''

import csv
import pickle

class Gff3(object):
    '''
    A class representing gff3 annotations
    '''

    def __init__(self, gff3_filepath):
        '''
        Constructor
        '''
        self.path = gff3_filepath

    def get_dic_subkeys(self):
        '''
        Get dic subkeys used to access elements in subdics when you index
        gff3 file
        '''
        chromo_str = 'chromo'
        feature_str = 'feature'
        start_str = 'start'
        end_str = 'end'
        strand_str = 'strand'
        attrib_str = 'attrib'
        return chromo_str, feature_str, start_str, end_str, strand_str, attrib_str

    def index(self, myfeature='miRNA', dickey='chrlocation', pkl_output_path=None, overwrite=False):
        '''
        Indexes gff3 file to a dictionary. Dictionary
        is of form:
        {
        chromo:chromosome_i,
        feature: feature_k (e.g. miRNA)
        start:
        end:
        strand:}

        Options:
        feature (type str): Only grab features that match this string.
        if None, does not filter by features

        pkl_output_path: writes output dictionary as
        pickle file to path. If None, it does not write.

        dickey: an integer. Specifies which column from gff3
        will from the dictionary's key. Default is 3, meaning
        it will have start location as dic key.

        setting dickey="chrlocation" will create a key of chr1:start:strand

        overwrite: force overwrite of pkl file, even if one exists already.
        '''
        #--------Begin: read lines as csv, collect chromosome, feature, start, end, strand
        gff3_dic = {}

        self.file = open(self.path, 'rb')
        self.reader = csv.reader(self.file, delimiter='\t')
        for row in self.reader:
            #Skip rows beginning with #
            if row[0].startswith('#'):
                # skip to next row
                continue
            '''
            Upcoming magic numbers are from gff3 file format
            Visit:
            https://www.broadinstitute.org/annotation/argo/help/gff3.html
            for how a gff3 file is structured
            '''
            feature = row[2]
            if feature == myfeature or None:
                pass
            else:
                # feature is not interesting to us, skip it.
                continue

            chromo = row[0]
            start = int(row[3])
            end = int(row[4])
            strand = row[6]
            attrib = row[8]
            # define key used to access dictionary
            if dickey == 'chrlocation':
                key = '%s:%s:%s' %(chromo, start, strand)
            else:
                key = row[dickey]

            # init subdic
            if key not in gff3_dic:
                gff3_dic[key] = {}
            else:    # complain
                print 'Warning: duplicate key: %s. \nOverwriting to new entry...' %key
            # define subkeys
            chromo_str, \
            feature_str, \
            start_str, \
            end_str, \
            strand_str, \
            attrib_str = self.get_dic_subkeys()

            for subkey, subval in \
                    zip([chromo_str, feature_str, start_str, end_str, strand_str, attrib_str],
                        [chromo, feature, start, end, strand, attrib]):
                gff3_dic[key][subkey] = subval

        #save dic to pickle, if you want.
        if pkl_output_path is not None:
            #only output if save path exists
            if os.path.exists(pkl_output_path):
                print '%s path exists.' %pkl_output_path
                if overwrite:
                    print 'Overwrite is ON, overwriting...'
                    pickle.dump(gff3_dic, open(pkl_output_path, 'wb'))
                    print 'Dic saved to %s.' %pkl_output_path
                else:
                    print 'Not overwriting. Set overwrite = True to ovewrite.'
            else:
                pickle.dump(gff3_dic, open(pkl_output_path, 'wb'))
                print 'Dic saved to %s.' %pkl_output_path
        return gff3_dic

