from PreprocessingPipeline.Transformers.Transformer import Transformer


class NormalizeExpressionByCell(Transformer):
    @property
    def file_suffix(self):
        return "NormalizeExpressionByCell"

    def transform_aux(self, expression_object, *args, **kwargs):
        expression_object.expression_matrix /= expression_object.expression_matrix.sum(axis=0)
        expression_object.name = self.out_file_name(expression_object.name)
        return expression_object
