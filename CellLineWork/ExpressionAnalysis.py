from CellLineWork.PreprocessExpressionMatrix import pre_process_expression_matrix
from Utilities import load_if_cached, join_paths
from config import BasePaths
from FilterExpressionByCellLine import filter_expression_by_cell_line
from sklearn.cluster import AgglomerativeClustering


class ExpressionAnalysis:
    def __init__(self, filter_by_cell_line=True):
        self.expression_matrix = load_if_cached(join_paths([BasePaths.ExpressionProcessed]),
                                                pre_process_expression_matrix)
        if filter_by_cell_line:
            self.expression_matrix, self.cell_lines_matrix, self.cell_lines_set = filter_expression_by_cell_line(
                self.expression_matrix)
            self.separated_expressions = {}
            for cell_line in self.cell_lines_set:
                self.separated_expressions[cell_line] = self.CellLineExpression(self.expression_matrix,
                                                                                self.cell_lines_matrix, cell_line)

    def cluster(self, per_cell_line=True):
        if per_cell_line:
            for expression in self.separated_expressions.values():
                expression.cluster()
        else:
            self.cluster = AgglomerativeClustering(linkage="average", compute_full_tree=True).fit(
                self.expression_matrix.transpose())

    class CellLineExpression:
        def __init__(self, expression_matrix, cell_lines_matrix, cell_line_name):
            self.cell_expression_matrix = expression_matrix.loc[:,
                                          cell_lines_matrix.loc[cell_lines_matrix["CellLine"] == cell_line_name][
                                              "sample_id"]]

        def cluster(self, method="Hierarchical"):
            if method == "Hierarchical":
                self.cluster_element = AgglomerativeClustering(linkage="average", compute_full_tree=True).fit(
                    self.cell_expression_matrix.transpose())


if __name__ == "__main__":
    E = ExpressionAnalysis()
    E.cluster()
    tmp = E.separated_expressions['NCIH2073_LUNG']
    print(tmp.cluster_element)
