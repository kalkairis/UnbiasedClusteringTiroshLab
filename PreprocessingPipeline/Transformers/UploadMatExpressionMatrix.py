import csv
import numpy as np
import pandas as pd

from PreprocessingPipeline.ExpressionAndMetaData.ExpressionMetaDataBase import ExpressionMetaDataBase
from PreprocessingPipeline.Transformers.Transformer import Transformer
import scipy.io as spio

from Utilities import join_paths
from config import BasePaths


class UploadMatExpressionMatrix(Transformer):
    def out_file_name(self, name=None):
        return self.file_suffix

    def __init__(self, expression_matrix_path=None, cell_matrix_path=None, cache_directory=BasePaths.Cache):
        self.expression_matrix_path = expression_matrix_path
        self.cell_matrix_path = cell_matrix_path
        self.composing_items.append(self.expression_matrix_path)
        self.composing_items.append(self.cell_matrix_path)
        self.cache_directory = cache_directory

    @property
    def file_suffix(self):
        return "FromMatExpressionMatrix"

    def transform_aux(self, expression_object, *args, **kwargs):
        expression_matrix = spio.mmread(self.expression_matrix_path)
        expression_matrix = expression_matrix.todense()
        expression_matrix = pd.DataFrame(expression_matrix)
        if self.cell_matrix_path is not None:
            cells_matrix = np.array([])
            with open(self.cell_matrix_path, 'r') as cells_matrix_file:
                cells_matrix_reader = csv.reader(cells_matrix_file, delimiter='\t')
                for row in cells_matrix_reader:
                    cells_matrix = np.append(cells_matrix, row)
        ret = ExpressionMetaDataBase(expression_matrix=expression_matrix, cells_matrix=cells_matrix)
        ret.name = self.file_suffix
        return ret

    def out_file_path(self, expression_object=None, *args, **kwargs):
        return join_paths([self.cache_directory, self.file_suffix])
