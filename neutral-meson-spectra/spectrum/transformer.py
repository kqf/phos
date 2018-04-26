from output import AnalysisOutput


class TransformerBase(object):

    def __init__(self, plot=True):
        super(TransformerBase, self).__init__()
        self.plot = plot

    def transform(self, inputs, loggs):
        lazy_logs = isinstance(loggs, basestring)

        if lazy_logs:
            loggs = AnalysisOutput(loggs)

        output = self.pipeline.transform(inputs, loggs)
        loggs.update('output', [output])

        if lazy_logs:
            loggs.plot(self.plot)

        return output
