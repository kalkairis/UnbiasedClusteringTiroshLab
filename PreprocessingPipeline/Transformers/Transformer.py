import pickle
from abc import ABCMeta, abstractmethod, abstractproperty


class Transformer(metaclass=ABCMeta):
    code_version = 1

    @abstractmethod
    def transform_aux(self, expression_object, *args, **kwargs):
        raise NotImplementedError

    def transform(self, expression_object, *args, **kwargs):
        out_file_name = expression_object.file_name + self.file_suffix
        try:
            ret = pickle.load(out_file_name)
            if ret.get_transformer_version() == self.code_version:
                return ret
            else:
                expression_object.log("Wrong code version of transformer, running transformer again")
                raise Exception
        except:
            expression_object.log("Running transformer {}".format(type(self)))
            ret = self.transform_aux(expression_object, args, kwargs)
            out_file_obj = open(out_file_name, 'w')
            pickle.dump(ret, out_file_obj)
            out_file_obj.close()
            expression_object.log(
                "Saved result from transformer {} with parameters {} in {}".format(type(self), self.composing_items,
                                                                                   out_file_obj))
            return ret

    @property
    def composing_items(self):
        return ()

    @property
    def file_suffix(self):
        raise NotImplementedError
