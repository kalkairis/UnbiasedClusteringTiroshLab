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
            with open(self.out_file_path(expression_object), 'rb') as in_file:
                ret = pickle.load(in_file)
            if ret.composing_items[-1] == self and ret.composing_items[:-1] == expression_object.composing_items:
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

    def out_file_name(self, name=None):
        if name is None:
            return self.file_suffix
        else:
            return name + '_' + self.file_suffix

    def out_file_path(self, expression_object=None, *args, **kwargs):
        if expression_object is None:
            return join_paths([BasePaths.Cache, self.out_file_name()])
        else:
            return join_paths([BasePaths.Cache, self.out_file_name(expression_object.name)])

    @property
    def composing_items(self):
        return [self.code_version]

    @property
    def file_suffix(self):
        raise NotImplementedError

    def __eq__(self, other):
        return type(self) == type(
            other) and self.code_version == other.code_version and self.composing_items == other.composing_items
