import pandas as pd

from config import BasePaths


def get_cohesive_cell_lines(cohesive_column_1, cohesive_column_2):
    cell_lines = pd.read_csv(BasePaths.CellLineExpression)
    cell_lines = cell_lines.loc[cell_lines.apply(lambda x: x[cohesive_column_1] == x[cohesive_column_2], axis=1)]
    return cell_lines.sample_id


if __name__ == "__main__":
    cohesive_sample_ids = get_cohesive_cell_lines('GE_CCLE_match', 'SNP_CL_match')
    expression_matrix =
