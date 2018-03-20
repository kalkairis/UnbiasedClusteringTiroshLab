from PreprocessingPipeline.PipelineBase import PipelineBase
from PreprocessingPipeline.Transformers.CellFilteringByReadsThreshold import CellFilteringByReadsThreshold
from PreprocessingPipeline.Transformers.FilterCohesiveCellsByCellLine import FilterCohesiveCellsByCellLine
from PreprocessingPipeline.Transformers.FilterGenesByPopulationExpression import FilterGenesByPopulationExpression
from PreprocessingPipeline.Transformers.NormalizeExpressionByCell import NormalizeExpressionByCell
from PreprocessingPipeline.Transformers.UploadMatExpressionMatrix import UploadMatExpressionMatrix
from config import BasePaths


class CellLineExpressionMatrix(PipelineBase):
    @property
    def name(self):
        return "CellLineExpressionMatrix"

    @property
    def pipeline_steps(self):
        return [
            UploadMatExpressionMatrix(expression_matrix_path=BasePaths.ExpressionMatMatrix,
                                      cell_matrix_path=BasePaths.BarCodes),
            NormalizeExpressionByCell(),
            CellFilteringByReadsThreshold(min_threshold=4000),
            FilterGenesByPopulationExpression(min_threshold=5),
            FilterCohesiveCellsByCellLine(cell_line_file_path=BasePaths.CellLineExpression,
                                          columns_to_compare=['GE_CCLE_match', 'SNP_CL_match'],
                                          cell_id_column="sample_id")
            # TODO: continue from here to work on transformer parts
        ]


if __name__ == "__main__":
    M = CellLineExpressionMatrix()
    X = M.execute()
    print(X.expression_matrix.head())
    print("bla")
