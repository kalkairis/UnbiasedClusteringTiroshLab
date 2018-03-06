from Utilities import *
import numpy as np
from config import BasePaths
import scipy.io as spio
import pandas as pd
import matplotlib.pyplot as plt
import os

DEBUG = False


def open_expression_mat():
    ret = spio.mmread(BasePaths.ExpressionMatMatrix)
    ret = ret.todense()
    ret = pd.DataFrame(data=ret)
    return ret


def visualize_num_genes_per_cell_distribution(num_genes_per_cell, out_file_name='num_genes_per_cell'):
    plt.subplot()
    num_genes_per_cell = sorted(num_genes_per_cell)
    plt.plot(range(len(num_genes_per_cell)), num_genes_per_cell)
    plt.xlabel("Cells")
    plt.ylabel("Number of Genes in cell")
    plt.savefig(join_paths([BasePaths.Images, out_file_name + '.png']))
    gradients = np.gradient(num_genes_per_cell)
    if DEBUG:
        plt.show()
    plt.subplot()
    plt.plot(range(len(gradients)), gradients, '-')
    plt.savefig(join_paths([BasePaths.Images, out_file_name + '_gradient_o_.png']))
    if DEBUG:
        plt.show()


def normalize_by_cell(exp_matrix):
    exp_matrix /= exp_matrix.sum(axis=0)
    return exp_matrix


def filter_cells(exp_matrix):
    num_genes_per_cell = (exp_matrix > 0).sum(axis=0)
    if DEBUG:
        visualize_num_genes_per_cell_distribution(num_genes_per_cell)
    filtered_by_cells_exp_matrix = exp_matrix.loc[:, num_genes_per_cell >= 4000]
    if DEBUG:
        visualize_num_genes_per_cell_distribution((filtered_by_cells_exp_matrix > 0).sum(axis=0),
                                                  'num_genes_per_cell_filtered')
    return filtered_by_cells_exp_matrix


def filter_genes(exp_matrix):
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
    plt.savefig(join_paths([BasePaths.Images, 'gene_count_distribution.png']))
    if DEBUG:
        plt.show()
    plt.show()
    return exp_matrix.loc[exp_matrix_values >= 5]


def pre_process_expression_matrix():
    print_log(os.getcwd(), DEBU)
    expression_matrix = open_expression_mat()
    expression_matrix = normalize_by_cell(expression_matrix)
    expression_matrix = filter_cells(expression_matrix)
    expression_matrix = filter_genes(expression_matrix)
    print_log(expression_matrix.head(), DEBUG)
    expression_matrix.to_pickle(join_paths([BasePaths.ExpressionProcessed]))
    return expression_matrix


if __name__ == "__main__":
    pre_process_expression_matrix()
