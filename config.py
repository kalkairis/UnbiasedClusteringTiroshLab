from Utilities import *
from sys import platform


class BasePaths:
    if platform.startswith("win"):
        RawDataFolder = join_paths(['D:', 'Box Sync', 'TiroshLab', 'RawData'])
    else:
        RawDataFolder = join_paths(['/home', 'labs', 'tirosh', 'iriska', 'RawData', 'CellLines'])
    Pilot19 = join_paths([RawDataFolder, 'pilot_19'])
    ExpressionMatMatrix = join_paths([Pilot19, 'matrix.mtx'])
    ExpressionProcessed = join_paths([Pilot19, 'expression_preprocessed_matrix.npy'])
    BarCodes = join_paths([Pilot19, 'barcodes.npy'])
    Images = join_paths([Pilot19, 'images'])