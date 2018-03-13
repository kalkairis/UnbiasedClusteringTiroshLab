import pickle
from abc import ABCMeta, abstractmethod, abstractproperty
import logging

from Utilities import join_paths
from config import BasePaths


class Transformer(metaclass=ABCMeta):
    code_version = 1

    @abstractmethod
    def transform_aux(self, expression_object, *args, **kwargs):
        raise NotImplementedError

    def transform(self, expression_object, *args, **kwargs):
        try:
            with open(self.out_file_path(expression_object), 'r') as in_file:
                ret = pickle.load(in_file)
            if ret.composing_items[-1].code_version == self.code_version:
                return ret
            else:
                logging.log("Wrong code version of transformer, running transformer again")
                raise Exception
        except:
            logging.info("Running transformer {}".format(type(self)))
            ret = self.transform_aux(expression_object, args, kwargs)
            ret.composing_items.append(self)
            with open(join_paths([BasePaths.Cache, ret.name]), 'wb') as out_file:
                pickle.dump(ret, out_file)
            logging.info(
                "Saved result from transformer {} with parameters {} in {}".format(type(self), self.composing_items,
                                                                                   self.out_file_path(
                                                                                       expression_object)))
            return ret

    def out_file_path(self, expression_object):
        return '_'.join([expression_object.name, self.file_suffix])

    @property
    def composing_items(self):
        return [self.code_version]

    @property
    def file_suffix(self):
        raise NotImplementedError
