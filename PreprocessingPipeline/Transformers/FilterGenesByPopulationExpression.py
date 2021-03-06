import numpy as np
import matplotlib.pyplot as plt
from PreprocessingPipeline.Transformers.Transformer import Transformer
from Utilities import join_paths
from config import BasePaths


class FilterGenesByPopulationExpression(Transformer):
    def __init__(self, min_threshold=None, max_threshold=None, cache_directory=BasePaths.Cache):
        super(FilterGenesByPopulationExpression, self).__init__(cache_dir=cache_directory)
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

    def plot_matrix(self, matrix):
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(len(matrix)), np.sort(matrix))
        ax.set(xlabel="Genes", ylabel="log2(TPM+1)")
        fig.savefig(join_paths([self.images_dir, 'gene_count_distribution.png']))
        fig, ax = plt.subplots(1,1)
        ax.hist(matrix)
        fig.savefig(join_paths([self.images_dir, 'gene_count_histogram.png']))

    def transform_aux(self, expression_object, *args, **kwargs):
        gene_sum_values = expression_object.expression_matrix.values
        gene_sum_values = gene_sum_values.mean(axis=1)
        gene_sum_values += 1
        gene_sum_values = np.log2(gene_sum_values)

        self.plot_matrix(gene_sum_values[np.nonzero(gene_sum_values)])
        keep_indices = [True] * len(gene_sum_values)
        if self.min_threshold is not None:
            keep_indices = np.logical_and(keep_indices, gene_sum_values >= self.min_threshold)
        if self.max_threshold is not None:
            keep_indices = np.logical_and(keep_indices, gene_sum_values <= self.max_threshold)
        expression_object.expression_matrix = expression_object.expression_matrix.loc[keep_indices]
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object

    @property
    def composing_items(self):
        ret = super(FilterGenesByPopulationExpression, self).composing_items
        ret.append((self.min_threshold, self.max_threshold))
        return ret
