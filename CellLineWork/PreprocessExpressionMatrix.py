from Utilities import *
from CellLineWork.UploadFiles import bar_codes_mat_to_numpy
import numpy as np
import config
from config import BasePaths
import scipy.io as spio
import pandas as pd
import matplotlib.pyplot as plt
import os


def open_expression_mat():
    ret = spio.mmread(BasePaths.ExpressionMatMatrix)
    ret = ret.todense()
    barcodes = load_if_cached(BasePaths.BarCodes, bar_codes_mat_to_numpy)
    print_log("barcodes: {}".format(barcodes), config.DEBUG)
    ret = pd.DataFrame(data=ret, columns=barcodes)
    return ret


def visualize_num_genes_per_cell_distribution(num_genes_per_cell, out_file_name='num_genes_per_cell',
                                              outdir=BasePaths.Images):
    fig, ax = plt.subplots(1, 1)
    num_genes_per_cell = sorted(num_genes_per_cell)
    ax.plot(range(len(num_genes_per_cell)), num_genes_per_cell)
    ax.set(xlabel="Cells", ylabel="Number of Genes in cell")
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    fig.savefig(join_paths([outdir, out_file_name + '.png']))
    gradients = np.gradient(num_genes_per_cell)
    if config.DEBUG:
        plt.show()
    fig, ax = plt.subplots(1, 1)
    ax.plot(range(len(gradients)), gradients, '-')
    fig.savefig(join_paths([outdir, out_file_name + '_gradient_o_.png']))
    if config.DEBUG:
        plt.show()


def normalize_by_cell(exp_matrix):
    exp_matrix /= exp_matrix.sum(axis=0)
    return exp_matrix


def filter_cells(exp_matrix):
    num_genes_per_cell = (exp_matrix > 0).sum(axis=0)
    if config.DEBUG:
        visualize_num_genes_per_cell_distribution(num_genes_per_cell)
    filtered_by_cells_exp_matrix = exp_matrix.loc[:, num_genes_per_cell >= 4000]
    if config.DEBUG:
        visualize_num_genes_per_cell_distribution((filtered_by_cells_exp_matrix > 0).sum(axis=0),
                                                  'num_genes_per_cell_filtered')
    return filtered_by_cells_exp_matrix


def filter_genes(exp_matrix, images_dir):
    exp_matrix_values = exp_matrix.values
    exp_matrix_values = exp_matrix_values.sum(axis=1)
    exp_matrix_values *= 10 ** 6
    exp_matrix_values += 1
    exp_matrix_values = np.log2(exp_matrix_values)

    exp_matrix_values_to_plot = exp_matrix_values[np.nonzero(exp_matrix_values)]
    plt.subplot()
    plt.plot(range(len(exp_matrix_values_to_plot)), np.sort(exp_matrix_values_to_plot))
    plt.xlabel("Genes")
    plt.ylabel("log2(TPM+1)")
    plt.savefig(join_paths([images_dir, 'gene_count_distribution.png']))
    if config.DEBUG:
        plt.show()
    plt.show()
    return exp_matrix.loc[exp_matrix_values >= 5]


if __name__ == "__main__":
    pre_process_expression_matrix()
