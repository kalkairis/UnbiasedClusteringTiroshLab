import csv
import numpy as np
import os
import pandas as pd

from PreprocessingPipeline.ExpressionAndMetaData.ExpressionMetaDataBase import ExpressionMetaDataBase
from PreprocessingPipeline.Transformers.Transformer import Transformer
import scipy.io as spio

from Utilities import join_paths
from config import BasePaths


class UploadMatExpressionMatrix(Transformer):
    def out_file_name(self, name=None):
        return self.file_suffix

    def __init__(self, dir_path_10x=BasePaths.Pilot19, cache_directory=BasePaths.Cache):
        super(UploadMatExpressionMatrix, self).__init__(cache_dir=cache_directory)
        self.dir_path_10x = dir_path_10x
        self.cache_directory = cache_directory
        self.expression_matrix_path = join_paths([self.dir_path_10x, 'matrix.mtx'])
        self.cell_matrix_path = join_paths([self.dir_path_10x, 'barcodes.tsv'])
        self.genes_matrix_path = join_paths([self.dir_path_10x, 'genes.tsv'])
        self.composing_items.append(self.expression_matrix_path)
        self.composing_items.append(self.cell_matrix_path)

    @property
    def file_suffix(self):
        return "FromMatExpressionMatrix"

    @staticmethod
    def read_tsv_file(path):
        ret = np.array([])
        with open(path, 'r') as in_file:
            in_file_reader = csv.reader(in_file, delimiter='\t')
            for row in in_file_reader:
                ret = np.append(ret, row)
        return ret

    def transform_aux(self, expression_object, *args, **kwargs):
        expression_matrix = spio.mmread(self.expression_matrix_path)
        expression_matrix = expression_matrix.todense()
        expression_matrix = pd.DataFrame(expression_matrix)
        if os.path.exists(self.cell_matrix_path):
            cells_matrix = self.read_tsv_file(self.cell_matrix_path)
        if os.path.exists(self.genes_matrix_path):
            genes_matrix = self.read_tsv_file(self.genes_matrix_path)

        ret = ExpressionMetaDataBase(expression_matrix=expression_matrix, cells_matrix=cells_matrix,
                                     genes_matrix=genes_matrix)
        ret.name = self.file_suffix
        return ret

    def out_file_path(self, expression_object=None, *args, **kwargs):
        return join_paths([self.cache_directory, self.file_suffix])

    ignore_debug = True
