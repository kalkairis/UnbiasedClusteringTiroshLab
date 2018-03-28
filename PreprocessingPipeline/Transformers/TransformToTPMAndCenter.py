from PreprocessingPipeline.Transformers.Transformer import Transformer
import numpy as np


class TransformToTPMAndCenter(Transformer):
    def transform_aux(self, expression_object, *args, **kwargs):
        expression_object.expression_matrix /= 10
        expression_object.expression_matrix += 1
        expression_object.expression_matrix = np.log2(expression_object.expression_matrix)
        expression_object.non_centered_expression_matrix = expression_object.expression_matrix.copy()
        delta_per_gene = expression_object.expression_matrix.mean(axis=1)
        expression_object.expression_matrix = expression_object.expression_matrix.sub(delta_per_gene.values, axis=0)
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object

    @property
    def file_suffix(self):
        return 'TPMCenteredForm'
