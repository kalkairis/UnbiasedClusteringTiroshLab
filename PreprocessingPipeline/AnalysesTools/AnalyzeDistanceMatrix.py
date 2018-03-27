from PreprocessingPipeline.AnalysesTools.BaseAnalysis import BaseAnalysis
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from Utilities import join_paths


class AnalyzeDistanceMatrix(BaseAnalysis):
    @property
    def name(self):
        return "AnalyzeDistanceMatrix"

    def plot_distance_distribution(self, distances, name=''):
        all_distances = distances.values
        upper_distances = np.triu(all_distances, k=0)
        upper_distances = upper_distances.reshape(-1)
        upper_distances = upper_distances[upper_distances > 0]
        plt.subplot()
        sns.distplot(upper_distances)
        plt.savefig(join_paths([self.outfile_path, name + 'distance_distribution.png']))

    def analyze(self, expression_object, **kwargs):
        distances = expression_object.distances
        self.plot_distance_distribution(distances, expression_object.name)
