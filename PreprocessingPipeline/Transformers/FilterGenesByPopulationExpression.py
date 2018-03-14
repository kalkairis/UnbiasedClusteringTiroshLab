import numpy as np
import matplotlib.pyplot as plt
from PreprocessingPipeline.Transformers.Transformer import Transformer
from Utilities import join_paths
from config import BasePaths


class FilterGenesByPopulationExpression(Transformer):
    def __init__(self, min_threshold=None, max_threshold=None):
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    @property
    def file_suffix(self):
        ret = "FilterGenesByPopulationExpression"
        if self.min_threshold is not None:
            ret += 'Min' + str(self.min_threshold)
        if self.max_threshold is not None:
            ret += 'Max' + str(self.max_threshold)
        return ret

    @staticmethod
    def plot_matrix(matrix):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(len(matrix)), np.sort(matrix))
        ax.xlabel("Genes")
        ax.ylabel("log2(TPM+1)")
        fig.savefig(join_paths([BasePaths.Images, 'gene_count_distribution.png']))

    def transform_aux(self, expression_object, *args, **kwargs):
        gene_sum_values = expression_object.expression_matrix.values
        gene_sum_values = gene_sum_values.sum(axis=1)
        gene_sum_values *= 10 ** 6
        gene_sum_values += 1
        gene_sum_values = np.log2(gene_sum_values)

        self.plot_matrix(gene_sum_values[np.nonzero(gene_sum_values)])
        keep_indices = [True] * len(gene_sum_values)
        if self.min_threshold is not None:
            keep_indices = np.logical_and(keep_indices, gene_sum_values >= self.min_threshold)
        if self.max_threshold is not None:
            keep_indices = np.logical_and(keep_indices, gene_sum_values <= self.max_threshold)
        expression_object.expression_matrix = expression_object.expression_matrix.loc[keep_indices]
        return expression_object

    @property
    def composing_items(self):
        ret = super(FilterGenesByPopulationExpression, self).composing_items
        ret.append((self.min_threshold, self.max_threshold))
        return ret
