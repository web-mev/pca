#! /usr/bin/python3

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
    parser.add_argument('-o', '--output', \
        required=True, \
        dest = 'output',
        help='The output PCA matrix'
    )
    parser.add_argument('-v', '--var', \
        required=True, \
        dest = 'exp_var_file',
        help='The file containing the explained variance ratio'
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    # read the input matrix:
    df = pd.read_table(args.input_matrix, index_col=0)

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
    t_df.to_csv(args.output, sep='\t')

    # explained variance:
    np.savetxt(args.exp_var_file, pca.explained_variance_ratio_)