import pandas as pd


class ExpressionMetaDataBase:
    def __init__(self, expression_matrix=None, cells_matrix=None, genes_matrix=None, composing_items=[]):
        self.expression_matrix = expression_matrix
        self.cells_matrix = cells_matrix
        self.genes_matrix = genes_matrix
        try:
            self.expression_matrix = self.expression_matrix.rename(columns=lambda x: self.cells_matrix[x],
                                                                   index=lambda x: self.genes_matrix[x])
        except:
            pass
        self.composing_items = composing_items

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
