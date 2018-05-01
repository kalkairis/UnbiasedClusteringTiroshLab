import sys
import os
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from PreprocessingPipeline.Transformers.TransformToTPMAndCenter import TransformToTPMAndCenter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PreprocessingPipeline.AnalysesTools.AnalyzeDistanceMatrix import AnalyzeDistanceMatrix
from PreprocessingPipeline.PipelineBase import PipelineBase
from PreprocessingPipeline.Transformers.CellFilteringByReadsThreshold import CellFilteringByReadsThreshold
from PreprocessingPipeline.Transformers.ClusterExpressionIntoTree import ClusterExpressionIntoTree
from PreprocessingPipeline.Transformers.ComputePairWiseDistances import ComputePairWiseDistances
from PreprocessingPipeline.Transformers.FilterCohesiveCellsByCellLine import FilterCohesiveCellsByCellLine
from PreprocessingPipeline.Transformers.FilterGenesByPopulationExpression import FilterGenesByPopulationExpression
from PreprocessingPipeline.Transformers.NormalizeExpressionByCell import NormalizeExpressionByCell
from PreprocessingPipeline.Transformers.UploadMatExpressionMatrix import UploadMatExpressionMatrix
from config import BasePaths


class CellLineExpressionMatrix(PipelineBase):
    def __init__(self, dir_path_10x=BasePaths.Pilot19,
                 min_reads_per_cell=4000, max_reads_per_cell=None,
                 minimal_mean_expression_of_gene=3,
                 maximal_mean_expression_of_gene=None,
                 cache_dir_path=BasePaths.Cache, cell_line_assignment_file=None,
                 cell_line_assignment_comparison_col1=None,
                 cell_line_assignment_comparison_col2=None, DEBUG=False):
        self.dir_path_10x = dir_path_10x
        self.min_reads_per_cell = min_reads_per_cell
        self.max_reads_per_cell = max_reads_per_cell
        self.minimal_mean_expression_of_gene = minimal_mean_expression_of_gene
        self.maximal_mean_expression_of_gene = maximal_mean_expression_of_gene
        self.cell_line_assignment_file = cell_line_assignment_file
        self.cell_line_assignment_comparison_col1 = cell_line_assignment_comparison_col1
        self.cell_line_assignment_comparison_col2 = cell_line_assignment_comparison_col2
        super(CellLineExpressionMatrix, self).__init__(cache_dir_path=cache_dir_path, DEBUG=DEBUG)

    @property
    def name(self):
        return "10xExpressionMatrix"

    @property
    def pipeline_steps(self):
        return [
            UploadMatExpressionMatrix(dir_path_10x=self.dir_path_10x, cache_directory=self.cache_dir),
            NormalizeExpressionByCell(cache_dir=self.cache_dir),
            CellFilteringByReadsThreshold(min_threshold=self.min_reads_per_cell, max_threshold=self.max_reads_per_cell,
                                          cache_directory=self.cache_dir),
            FilterGenesByPopulationExpression(min_threshold=self.minimal_mean_expression_of_gene,
                                              max_threshold=self.maximal_mean_expression_of_gene,
                                              cache_directory=self.cache_dir),
            TransformToTPMAndCenter(cache_dir=self.cache_dir),
            # TODO: continue from here to work on transformer parts
        ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Arguments for analyzing cell line expression matrices \nNOTICE: currently works only for 10x!!")
    parser.add_argument('--dir_path_10x', dest='dir_path_10x', action='store',
                        help='Absolute path of 10X output directory including:'
                             '\n1. matrix.mtx Matlab expression matrix'
                             '\n2. barcodes.tsv Matlab barcodes of cells'
                             '\n3. genes.tsv Matlab genes',
                        default=BasePaths.ExpressionMatMatrix)
    parser.add_argument('--min_reads_per_cell', action='store', dest='min_reads_per_cell', type=int,
                        help='Minimal number of reads in cells, cells with less reads than threshold will be discarded',
                        default=4000)
    parser.add_argument('--max_reads_per_cell', action='store', dest='max_reads_per_cell', type=int,
                        help='Maximal number of reads in cells, cells with more reads than threshold will be discarded',
                        default=None)
    parser.add_argument('--minimal_mean_expression_of_gene', action='store', dest='minimal_mean_expression_of_gene',
                        type=float,
                        help='Minimal mean expression per gene, those with lower expression will be discarded',
                        default=3)
    parser.add_argument('--maximal_mean_expression_of_gene', action='store', dest='maximal_mean_expression_of_gene',
                        type=float,
                        help='Maximal mean expression per gene, those with higher expression will be discarded',
                        default=None)
    parser.add_argument('--cache_dir_path', action='store', dest='cache_dir_path',
                        help='Absolute path for cache directory',
                        default=BasePaths.Cache)
    parser.add_argument('--cell_line_assignment_file', action='store', dest='cell_line_assignment_file',
                        help='If separating to different origins then the path of'
                             ' CSV containing the different assignments.'
                             '\nNotice you will also need to set the names of assignments to use.',
                        default=None)
    parser.add_argument('--cell_line_assignment_comparison_col1', action='store',
                        dest='cell_line_assignment_comparison_col1',
                        help='First column to compare cell line assignments', default=None)
    parser.add_argument('--cell_line_assignment_comparison_col2', action='store',
                        dest='cell_line_assignment_comparison_col2',
                        help='Second column to compare cell line assignments', default=None)
    parser.add_argument('--DEBUG', dest='DEBUG', action='store_true', default=False)
    args = parser.parse_args()
    print(*args.__dict__)
    M = CellLineExpressionMatrix(**args.__dict__)
    X = M.execute()
    X.expression_matrix.to_csv(os.path.join(args.__dict__['cache_dir_path'], 'FilteredExpressionMatrix.csv'))
    print('done')
