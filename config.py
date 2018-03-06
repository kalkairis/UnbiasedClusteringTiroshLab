from Utilities import *


class BasePaths:
    RawDataFolder = join_paths(['D:', 'Box Sync', 'TiroshLab', 'RawData'])
    Pilot19 = join_paths([RawDataFolder, 'pilot_19'])
    ExpressionMatMatrix = join_paths([Pilot19, 'matrix.mtx'])
    ExpressionProcessed = join_paths([Pilot19, 'expression_preprocessed_matrix.npy'])
    CellLineExpression = join_paths([Pilot19, 'expt1_data.csv'])
    BarCodes = join_paths([Pilot19, 'barcodes.npy'])
    Images = join_paths([Pilot19, 'images'])
