from abc import ABCMeta, abstractproperty
from Utilities import *

import logging


class ExpressionMetaDataBase(metaclass=ABCMeta):
    code_version = 1
    DEBUG = False

    def __init__(self):
        logging.basicConfig(filename=self.log_file_name)

    @property
    def log_file_name(self):
        return 'log.out'

    @property
    def pickle_dump_path(self):
        pass

    @property
    def expression_matrix_path(self):
        pass

    @property
    def composing_items(self):
        return [self.code_version, ]

    def get_transformer_version(self):
        return self.code_version

    @staticmethod
    def log(self, message):
        logging.log(message)
        print_log(message, self.DEBUG)

    def get_matrix(self):
        # TODO: continue here
        pass
