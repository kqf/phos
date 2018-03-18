class TransformerBase(object):

    def transform(self, inputs, loggs):
        output = self.pipeline.transform(inputs, loggs)
        return output