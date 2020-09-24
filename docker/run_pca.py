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

if __name__ == '__main__':
    args = parse_args()

    # read the input matrix:
    working_dir = os.path.dirname(args.input_matrix)
    f = os.path.join(working_dir, args.input_matrix)
    if os.path.exists(f):
        df = pd.read_table(f, index_col=0)
    else:
        sys.stderr.write('Could not find file: %s' % f)
        sys.exit(1)

    # if a subset of samples was requested, subset the matrix:
    if args.samples:
        samples_from_mtx = set(df.columns.tolist())
        requested_sample_list = [x.strip() for x in args.samples.split(',')]
        requested_sample_set = set(requested_sample_list)
        if len(requested_sample_set.difference(samples_from_mtx)) > 0:
            raise Exception('Requested samples differed from those in matrix.')
        df = df[requested_sample_list]

    # now run the PCA
    pca = PCA(n_components=2)

    # the fit_transform method expects a (samples, features) orientation
    t_df = pd.DataFrame(
        pca.fit_transform(df.T), 
        index=df.columns, 
        columns=['pc1', 'pc2']
    )
    fout = os.path.join(working_dir, 'pca_output.tsv')
    t_df.to_csv(fout, sep='\t')

    outputs = {
        'pca_coordinates': fout,
        'pc1_explained_variance':pca.explained_variance_ratio_[0],
        'pc2_explained_variance': pca.explained_variance_ratio_[1]
    }
    json.dump(outputs, open(os.path.join(working_dir, 'outputs.json'), 'w'))
