from PreprocessingPipeline.PipelineBase import PipelineBase
from PreprocessingPipeline.Transformers.CellFilteringByReadsThreshold import CellFilteringByReadsThreshold
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
            CellFilteringByReadsThreshold(min_threshold=4000)
# TODO: continue from here to work on transformer parts
        ]


if __name__ == "__main__":
    M = CellLineExpressionMatrix()
    X = M.execute()
    print(X.expression_matrix.head())
    print("bla")
