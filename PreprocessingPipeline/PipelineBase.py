import pickle
from abc import ABCMeta

import logging
from datetime import datetime

from PreprocessingPipeline.ExpressionAndMetaData.ExpressionMetaDataBase import ExpressionMetaDataBase
import config
from config import BasePaths
from Utilities import *


def pipeline_load_if_exists(path, name, composing_items):
    try:
        with open(join_paths([path, name])) as in_file:
            ret = pickle.load(in_file)
        if len(composing_items) == len(ret.composing_items) and all(
                [type(x[0]) == type(x[1]) and x[0].composing_items == x[1].composing_items for x in
                 zip(composing_items, ret.composing_items)]):
            return ret
    except:
        return None


class PipelineBase(metaclass=ABCMeta):
    code_version = 1

    def __init__(self, input_matrix=None, cache_dir_path=BasePaths.Cache, DEBUG=False):
        self.ExpressionMatrixFirstElement = input_matrix
        self.ExpressionMatrixElement = None
        self.cache_dir = cache_dir_path
        self.DEBUG = DEBUG
        self.log_path = join_paths([cache_dir_path, self.name + datetime.now().strftime("%Y_%m_%d_%H_%M") + ".log"])
        if not os.path.exists(cache_dir_path):
            print("trying to create {} directory".format(cache_dir_path))
            os.makedirs(cache_dir_path)
        log_file = open(self.log_path, 'w')
        log_file.close()
        logging.basicConfig(filename=self.log_path)
        print(f"Logging into {self.log_path}")

    @property
    def pipeline_steps(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    def execute(self):
        if self.ExpressionMatrixElement is not None:
            return self.ExpressionMatrixElement
        try:
            if self.DEBUG:
                raise IOError
            with open(join_paths([self.cache_dir, self.name]), 'rb') as in_file:
                self.ExpressionMatrixElement = pickle.load(in_file)
            if len(self.pipeline_steps) == len(self.ExpressionMatrixElement.composing_items) and all(
                    [type(x[0]) == type(x[1]) and x[0].composing_items == x[1].composing_items for x in
                     zip(self.ExpressionMatrixElement.composing_items, self.pipeline_steps)]):
                return self.ExpressionMatrixElement
            else:
                logging.info("Pipeline is different than current pipeline, creating new instance")
                print("Pipeline is different than current pipeline, creating new instance")
                raise Exception
        except:
            logging.info("Creating new instance of expression matrix")
            print("Creating new instance of expression matrix")
            ret = self.ExpressionMatrixFirstElement
            if ret is None:
                ret = ExpressionMetaDataBase()
            ret.name = self.name
            for i, pipeline_step in enumerate(self.pipeline_steps):
                # tmp = pipeline_load_if_exists()
                logging.info("Running pipeline step {}".format(type(pipeline_step)))
                print("Running pipeline step {}".format(type(pipeline_step)))
                ret = pipeline_step.transform(ret)
                logging.info("Finished pipeline step {}".format(type(pipeline_step)))
                "Finished pipeline step {}".format(type(pipeline_step))
            self.ExpressionMatrixElement = ret
            with open(join_paths([self.cache_dir, self.name]), 'wb') as out_file:
                pickle.dump(self.ExpressionMatrixElement, out_file)
            return ret
