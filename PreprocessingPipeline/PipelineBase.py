import pickle
from abc import ABCMeta

import logging
from datetime import datetime

from config import BasePaths
from Utilities import *


class PipelineBase(metaclass=ABCMeta):
    code_version = 1

    def __init__(self, input_matrix=''):
        self.ExpressionMatrixFirstElement = input_matrix
        self.ExpressionMatrixElement = None
        self.log_path = join_paths([BasePaths.Cache, self.name + datetime.now().strftime("%Y_%m_%d_%H_%M") + ".log"])
        if not os.path.exists(BasePaths.Cache):
            os.makedirs(BasePaths.Cache)
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
            with open(join_paths([BasePaths.Cache, self.name]), 'rb') as in_file:
                self.ExpressionMatrixElement = pickle.load(in_file)
            if len(self.pipeline_steps) == len(self.ExpressionMatrixElement.composing_items) and all(
                    [type(x[0]) == type(x[1]) and x[0].composing_items == x[1].composing_items for x in
                     zip(self.ExpressionMatrixElement.composing_items, self.pipeline_steps)]):
                return self.ExpressionMatrixElement
            else:
                logging.info("Pipeline is different than current pipeline, creating new instance")
                print("Pipeline is different than current pipeline, creating new instance")
        except:
            logging.info("Creating new instance of expression matrix")
            print("Creating new instance of expression matrix")
            ret = self.ExpressionMatrixFirstElement
            for pipeline_step in self.pipeline_steps:
                logging.info("Running pipeline step {}".format(type(pipeline_step)))
                print("Running pipeline step {}".format(type(pipeline_step)))
                ret = pipeline_step.transform(ret)
                logging.info("Finished pipeline step {}".format(type(pipeline_step)))
                "Finished pipeline step {}".format(type(pipeline_step))
            self.ExpressionMatrixElement = ret
            with open(join_paths([BasePaths.Cache, self.name]), 'wb') as out_file:
                pickle.dump(self.ExpressionMatrixElement, out_file)
            return ret
