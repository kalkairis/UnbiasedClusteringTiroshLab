import pandas as pd

from CellLineWork.PreprocessExpressionMatrix import pre_process_expression_matrix
from Utilities import *
from config import BasePaths

DEBUG = True


def get_cohesive_cell_lines(cohesive_column_1, cohesive_column_2):
    cell_lines = pd.read_csv(BasePaths.CellLineExpression)
    cell_lines = cell_lines.loc[cell_lines.apply(lambda x: x[cohesive_column_1] == x[cohesive_column_2], axis=1)]
    print_log("cell lines: {}".format(cell_lines.head()), DEBUG)
    return cell_lines.sample_id, cell_lines[["sample_id", cohesive_column_1]].rename(columns={cohesive_column_1:
                                                                                                  "CellLine"})


def filter_expression_by_cell_line(exp_matrix, cell_lines_columns=('GE_CCLE_match', 'SNP_CL_match')):
    cohesive_sample_ids, cell_lines_mat = get_cohesive_cell_lines(*cell_lines_columns)
    print_log(cohesive_sample_ids.head(), DEBUG)

    print_log("expression matrix shape: {}".format(exp_matrix.shape), DEBUG)
    exp_matrix = exp_matrix.loc[:, cohesive_sample_ids.values]
    print_log("expression matrix shape: {}".format(exp_matrix.shape), DEBUG)
    print_log(exp_matrix.head(), DEBUG)
    cell_lines_sets = set(cell_lines_mat["CellLine"].values)
    print_log("existing cell lines: {}".format(cell_lines_sets), DEBUG)
    return exp_matrix, cell_lines_mat, cell_lines_sets


if __name__ == "__main__":
    expression_matrix = load_if_cached(join_paths([BasePaths.ExpressionProcessed]), pre_process_expression_matrix)
    expression_matrix, cell_lines_matrix, cell_lines_set = filter_expression_by_cell_line(expression_matrix)
