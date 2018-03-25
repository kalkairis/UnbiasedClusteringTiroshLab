from abc import ABCMeta, abstractmethod

from config import BasePaths


class BaseAnalysis(metaclass=ABCMeta):
    def __init__(self, outfile_path = BasePaths.Images):
        self.outfile_path = outfile_path

    @property
    def name(self):
        raise NotImplementedError

    code_version = 1

    @property
    def composing_items(self):
        return [self.code_version]

    @abstractmethod
    def analyze(self, **kwargs):
        raise NotImplementedError
