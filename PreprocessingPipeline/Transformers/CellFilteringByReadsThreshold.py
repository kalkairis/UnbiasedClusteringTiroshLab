from CellLineWork.PreprocessExpressionMatrix import visualize_num_genes_per_cell_distribution
from PreprocessingPipeline.Transformers.Transformer import Transformer
from config import BasePaths


class CellFilteringByReadsThreshold(Transformer):
    def __init__(self, min_threshold=None, max_threshold=None, cache_directory=BasePaths.Cache):
        super(CellFilteringByReadsThreshold, self).__init__(cache_dir=cache_directory)
        if min_threshold is None and max_threshold is None:
            raise IOError("Filtering cells by threshold needs a threshold")
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    @property
    def file_suffix(self):
        ret = "CellFilteringByReadsThreshold"
        if self.min_threshold is not None:
            ret += 'min' + str(self.min_threshold)
        if self.max_threshold is not None:
            ret += 'max' + str(self.max_threshold)
        return ret

    def transform_aux(self, expression_object, *args, **kwargs):
        num_genes_per_cell = (expression_object.expression_matrix > 0).sum(axis=0)
        visualize_num_genes_per_cell_distribution(num_genes_per_cell)
        if self.min_threshold is not None:
            expression_object.expression_matrix = expression_object.expression_matrix.loc[:,
                                                  num_genes_per_cell >= self.min_threshold]
        if self.max_threshold is not None:
            expression_object.expression_matrix = expression_object.expression_matrix.loc[:,
                                                  num_genes_per_cell <= self.max_threshold]
        visualize_num_genes_per_cell_distribution((expression_object.expression_matrix > 0).sum(axis=0),
                                                  'num_genes_per_cell_filtered', self.images_dir)
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object

    @property
    def composing_items(self):
        return super(CellFilteringByReadsThreshold, self).composing_items.append(
            (self.min_threshold, self.max_threshold))
