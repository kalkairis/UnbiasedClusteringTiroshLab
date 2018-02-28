from sklearn.manifold import TSNE
import seaborn as sns
from Utilities import *
import numpy as np

DEBUG = True


def print_log(message):
    if DEBUG:
        print(message)


if __name__ == '__main__':
    print_log('loading expression matrix')
    expression_matrix = np.load(join_paths(['..', 'RawData', 'pilot_19', 'expression_preprocessed_matrix.npy']))
    print_log('loaded expression matrix')
    expression_tSNE = TSNE(n_components=2).fit_transform(expression_matrix)
    print_log('finished calculating tSNE')
    print(expression_tSNE.head())
    print_log('cluster mapping')
    sns.clustermap(expression_tSNE)
    print_log('finished cluster mapping')
    print('done')
