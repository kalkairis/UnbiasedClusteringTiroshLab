import getpass
from collections import defaultdict

from Utilities import *
from sys import platform


def get_user_name():
    name_dictionary = defaultdict(lambda x: x)
    name_dictionary['iriskalka'] = 'iriska'
    return name_dictionary[getpass.getuser()]


class BasePaths:
    if platform.startswith("win"):
        RawDataFolder = join_paths(['D:', 'Box Sync', 'TiroshLab', 'RawData'])
        UserFolder = join_paths(['D:', 'Box Sync', 'TiroshLab'])
    elif platform == 'linux':
        RawDataFolder = join_paths(['/home', 'labs', 'tirosh', 'itayt', 'cell_lines'])
    elif platform == "darwin":
        # RawDataFolder = join_paths()
        pass
        UserFolder = join_paths(['/home', 'labs', 'tirosh', getpass.getuser()])
    elif platform == 'darwin':
        RawDataFolder = join_paths(['/Volumes', 'cell_lines'])
        UserFolder = join_paths(['/Volumes', get_user_name()])
    Pilot19 = join_paths([RawDataFolder, 'pilot_19'])
    ExpressionMatMatrix = join_paths([Pilot19, 'matrix.mtx'])
    ExpressionProcessed = join_paths([Pilot19, 'expression_preprocessed_matrix.npy'])
    CellLineExpression = join_paths([Pilot19, 'expt1_data.csv'])
    BarCodes = join_paths([Pilot19, 'barcodes.tsv'])
    Cache = join_paths([UserFolder, 'PipelineCache'])
    Images = join_paths([Cache, 'images'])
