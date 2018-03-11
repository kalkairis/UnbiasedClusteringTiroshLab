from Utilities import *
from config import BasePaths
import numpy as np
import csv


def bar_codes_mat_to_numpy(bar_codes_numpy_path=BasePaths.BarCodes,
                           bar_codes_matlab_path=join_paths([BasePaths.Pilot19, 'barcodes.tsv'])):
    """

    :param bar_codes_numpy_path: str
    :type bar_codes_matlab_path: str
    """
    bar_codes = np.array([])
    with open(bar_codes_matlab_path, 'r') as barcode_file:
        barcode_reader = csv.reader(barcode_file, delimiter='\t')
        for row in barcode_reader:
            bar_codes = np.append(bar_codes, row)
    bar_codes.save(bar_codes_numpy_path)
    return bar_codes
