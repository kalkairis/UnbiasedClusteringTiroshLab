from os.path import join
import os
import pandas as pd
import numpy as np


def join_paths(paths):
    ret = ''
    for path in paths:
        if len(ret) == 0:
            ret = path
        else:
            ret = join(ret, path)
    return ret


def load_if_cached(path, created_function):
    if os.path.exists(path):
        try:
            return pd.read_pickle(path)
        except:
            return np.load(path)
    else:
        return created_function()


def print_log(message, DEBUG):
    if DEBUG:
        print(message)
