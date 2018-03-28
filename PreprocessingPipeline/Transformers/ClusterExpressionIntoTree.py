from PreprocessingPipeline.Transformers.Transformer import Transformer
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from config import BasePaths
from Utilities import *


class ClusterExpressionIntoTree(Transformer):
    def transform_aux(self, expression_object, *args, **kwargs):
        tree = linkage(expression_object.expression_matrix)
        fig = plt.figure()
        try:
            dn = dendrogram(tree)
            plt.show()
        except:
            try:
                plt.savefig(join(BasePaths.Images, "dendrogram.png"))
            except:
                print("Did not manage to create or save dendrogram")
        expression_object.tree = tree
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object

    @property
    def file_suffix(self):
        return 'ClusteredExpression'
