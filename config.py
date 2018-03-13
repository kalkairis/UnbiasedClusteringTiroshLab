import getpass

from Utilities import *
from sys import platform


class BasePaths:
    if platform.startswith("win"):
        RawDataFolder = join_paths(['D:', 'Box Sync', 'TiroshLab', 'RawData'])
    elif platform=='linux':
        RawDataFolder = join_paths(['/home', 'labs', 'tirosh', 'itayt', 'cell_lines'])
    Pilot19 = join_paths([RawDataFolder, 'pilot_19'])
    ExpressionMatMatrix = join_paths([Pilot19, 'matrix.mtx'])
    ExpressionProcessed = join_paths([Pilot19, 'expression_preprocessed_matrix.npy'])
    CellLineExpression = join_paths([Pilot19, 'expt1_data.csv'])
    BarCodes = join_paths([Pilot19, 'barcodes.tsv'])
    Cache = join_paths(['/home', 'labs', 'tirosh', getpass.getuser(), 'PipelineCache'])
    Images = join_paths([Cache, 'images'])

