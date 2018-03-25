from PreprocessingPipeline.Transformers.Transformer import Transformer
import pandas as pd
import numpy as np


class FilterCohesiveCellsByCellLine(Transformer):
    def __init__(self, cell_line_file_path, columns_to_compare, cell_id_column="sample_id"):
        self.cell_line_file_path = cell_line_file_path
        self.columns_to_compare = columns_to_compare
        self.cell_id_column = cell_id_column
        self.cell_lines = self.get_cohesive_cell_lines()

    @property
    def composing_items(self):
        ret = super(FilterCohesiveCellsByCellLine, self).composing_items
        ret.append(self.cell_line_file_path)
        ret.append(self.columns_to_compare)
        ret.append(self.cell_id_column)
        return ret

    def get_cohesive_cell_lines(self):
        cell_lines = pd.read_csv(self.cell_line_file_path)
        cohesive_cells_lines = cell_lines.loc[
            cell_lines.apply(lambda x: len(np.unique(x[self.columns_to_compare])) == 1, axis=1)]
        return cohesive_cells_lines[[self.cell_id_column, self.columns_to_compare[0]]].rename(
            columns={self.columns_to_compare[0]: "CellLine"})

    def transform_aux(self, expression_object, *args, **kwargs):
        cohesive_cell_indices = list(map(lambda x: x in self.cell_lines.sample_id.values, expression_object.cells_matrix))
        cohesive_cell_indices = [c[0] for c in enumerate(cohesive_cell_indices) if c[1]]
        expression_object.expression_matrix = expression_object.expression_matrix.loc[:, cohesive_cell_indices]
        expression_object.cells_metadata = self.cell_lines
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object

    @property
    def file_suffix(self):
        return "FilterCohesiveCellsByCellLine"
