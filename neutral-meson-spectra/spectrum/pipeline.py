from comparator import Comparator
from broot import BROOT as br
from output import AnalysisOutput


class HistogramSelector(object):

    def __init__(self, histname):
        super(HistogramSelector, self).__init__()
        self.histname = histname

    def transform(self, inputs, loggs):
        output = inputs._asdict()[self.histname]
        return output


class Pipeline(object):

    def __init__(self, steps):
        super(Pipeline, self).__init__()
        self.steps = steps

    def transform(self, inputs, loggs):
        updated = inputs
        for name, step in self.steps:
            local_logs = AnalysisOutput(name)
            updated = step.transform(updated, loggs)
            loggs.append(local_logs)
        return updated


class ParallelPipeline(object):

    def __init__(self, steps):
        super(ParallelPipeline, self).__init__()
        self.steps = steps

    def transform(self, inputs, loggs):
        assert len(inputs) == len(self.steps), "Input shape doesn't match the shape of estimators"

        def tr(x, name, step, loggs):
            local_logs = AnalysisOutput(name)
            output = step.transform(x, local_logs) 
            print "Printing local logs", local_logs
            loggs.append(local_logs)
            return output

        outputs = [ tr(inp, name, step, loggs)
            for inp, (name, step) in zip(inputs, self.steps)
        ]
        return outputs


class ReducePipeline(object):

    def __init__(self, parallel, function):
        super(ReducePipeline, self).__init__()
        self.parallel = parallel
        self.function = function 

    def transform(self, inputs, loggs):
        updated = self.parallel.transform(inputs, loggs)
        return self.function(updated) 


class RatioUnion(object):

    def __init__(self, numerator, denominator, error="B"):
        super(RatioUnion, self).__init__()
        self.numerator = numerator
        self.denominator = denominator
        self.error = error

    def transform(self, inputs, loggs):
        numerator = self.numerator.transform(inputs, loggs)
        denominator = self.denominator.transform(inputs, loggs)

        numerator, denominator = br.rebin_as(numerator, denominator)
        br.scalew(denominator)
        br.scalew(numerator)
        return br.ratio(numerator, denominator, self.error)

