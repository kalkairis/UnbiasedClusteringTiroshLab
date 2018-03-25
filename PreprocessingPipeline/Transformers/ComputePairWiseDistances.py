from PreprocessingPipeline.Transformers.Transformer import Transformer
import numpy as np


class ComputePairWiseDistances(Transformer):
    def transform_aux(self, expression_object, *args, **kwargs):
        expression_mat = expression_object.expression_matrix
        distances = expression_mat.apply(
            lambda x: expression_mat.apply(lambda y: self.distance_methods[self.distance_method](x, y),
                                           axis=self.axis_conversions[self.axis]),
            axis=self.axis_conversions[self.axis])
        expression_object.distances = distances
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object

    @property
    def axis_conversions(self):
        return {'cells': 0, 'genes': 1}

    @property
    def distance_methods(self):
        return {'euclidean': self.euclidean_distance}

    def __init__(self, distance_method='euclidean', axis='cells'):
        '''
        :param distance_method: distance calculation method. Available options include: 'euclidean'
        :param axis: Should the pairwise distances be between "cells" or between "genes"
        '''
        assert distance_method in self.distance_methods.keys(), 'distance must be in {}'.format(
            self.distance_methods.keys())
        self.distance_method = distance_method
        assert axis in self.axis_conversions.keys(), 'axis must be in {}'.format(self.axis_conversions.keys())
        self.axis = axis

    @property
    def file_suffix(self):
        return 'PairWiseDistances' + str(self.distance_method)

    @property
    def composing_items(self):
        return super(ComputePairWiseDistances, self).composing_items.append(self.distance_method)

    @staticmethod
    def euclidean_distance(element_1, element_2):
        dist = np.linalg.norm(element_1 - element_2)
        return dist
