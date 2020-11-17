#! /usr/bin/python3

import sys
import os
import json
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import argparse

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', \
        required=True, \
        dest = 'input_matrix',
        help='The input matrix'
    )
    parser.add_argument('-s', '--samples', \
        required=False, \
        dest = 'samples',
        help=('A comma-delimited list of the samples to run PCA on. Without'
            ' this argument, PCA is run on all samples.'
        )
    )
    args = parser.parse_args()
    return args

def get_file_reader(filename):
    '''
    Takes a filename and gets the file parser based on the extension.
    '''
    file_extension = filename.split('.')[-1].lower()

    if file_extension == 'csv':
        return pd.read_csv
    elif file_extension in ['tsv', 'tab']:
        return pd.read_table
    elif file_extension in ['xls', 'xlsx']:
        return pd.read_excel
    else:
        sys.stderr.write('Could not determine a file parser from the extension: %s' % file_extension)
        sys.exit(1)

if __name__ == '__main__':
    args = parse_args()

    # read the input matrix:
    working_dir = os.path.dirname(args.input_matrix)
    f = os.path.join(working_dir, args.input_matrix)
    if os.path.exists(f):
        reader = get_file_reader(os.path.basename(f))
        df = reader(f, index_col=0)
    else:
        sys.stderr.write('Could not find file: %s' % f)
        sys.exit(1)

    # if a subset of samples was requested, subset the matrix:
    if args.samples:
        samples_from_mtx = set(df.columns.tolist())
        requested_sample_list = [x.strip() for x in args.samples.split(',')]
        requested_sample_set = set(requested_sample_list)
        difference_set = requested_sample_set.difference(samples_from_mtx)
        if len(difference_set) > 0:
            sys.stderr.write('Requested samples differed from those in matrix: {csv}'.format(
                csv = ','.join(difference_set)
            ))
            sys.exit(1)
        df = df[requested_sample_list]

    # now run the PCA
    pca = PCA(n_components=2)

    try:
        # the fit_transform method expects a (samples, features) orientation
        transformed = pca.fit_transform(df.T)
    except Exception as ex:
        sys.stderr.write('Encountered an exception while calculating the princpal components. Exiting.')
        sys.exit(1)

    t_df = pd.DataFrame(
        transformed.T, # note the transform so the resulting matrix matches our convention (Samples in cols)
        columns=df.columns, 
        index=['pc1', 'pc2']
    )
    fout = os.path.join(working_dir, 'pca_output.tsv')
    t_df.to_csv(fout, sep='\t')

    outputs = {
        'pca_coordinates': fout,
        'pc1_explained_variance':pca.explained_variance_ratio_[0],
        'pc2_explained_variance': pca.explained_variance_ratio_[1]
    }
    json.dump(outputs, open(os.path.join(working_dir, 'outputs.json'), 'w'))
