from comparator import Comparator
from broot import BROOT as br
from output import AnalysisOutput, MergedLogItem
from transformer import TransformerBase


class HistogramSelector(object):

    def __init__(self, histname):
        super(HistogramSelector, self).__init__()
        self.histname = histname

    def transform(self, inputs, loggs):
        output = inputs._asdict()[self.histname]
        return output

class HistogramScaler(object):

    def __init__(self, factor):
        super(HistogramScaler, self).__init__()
        self.factor = factor

    def transform(self, inputs, loggs):
        inputs.Scale(self.factor)
        return inputs


class FunctionTransformer(object):

    def __init__(self, func):
        super(FunctionTransformer, self).__init__()
        self.func = func

    def transform(self, inputs, loggs):
        output = self.func(inputs)
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
        assert len(inputs) == len(self.steps), "Input shape doesn't match the shape of estimators, got {0}, {1}".format(
            len(inputs),
            len(self.steps)
        )

        def tr(x, name, step, loggs):
            local_logs = AnalysisOutput(name)
            output = step.transform(x, local_logs)
            # print "Printing local logs", local_logs
            loggs.append(local_logs)
            return output, local_logs.mergelist()

        output_with_logs = [ tr(inp, name, step, loggs)
            for inp, (name, step) in zip(inputs, self.steps)
        ]

        outputs, local_logs = zip(*output_with_logs)

        merged_loggs = AnalysisOutput(loggs.label)
        merged_loggs.pool = [MergedLogItem("merged", local)
            for local in zip(*local_logs)
        ]
        loggs.append(merged_loggs)
        return outputs


class ReducePipeline(object):

    def __init__(self, parallel, function):
        super(ReducePipeline, self).__init__()
        self.parallel = parallel
        self.function = function

    def transform(self, inputs, loggs):
        updated = self.parallel.transform(inputs, loggs)
        loggs.update("reduced_output", [updated])
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
        loggs.update("ratio_union", [[numerator, denominator]])
        return br.ratio(numerator, denominator, self.error)
