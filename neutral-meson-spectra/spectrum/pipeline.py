from comparator import Comparator
from broot import BROOT as br
from output import AnalysisOutput, MergedLogItem
from transformer import TransformerBase
import sutils as st


class ComparePipeline(TransformerBase):

    def __init__(self, estimators, plot=False, **kwargs):
        super(ComparePipeline, self).__init__(plot)
        self.estimators = estimators
        self.labels = zip(*estimators)[0]
        self.kwargs = kwargs

    def transform(self, data, loggs):
        self.pipeline = ReducePipeline(
            ParallelPipeline(self.estimators),
            Comparator(
                labels=self.labels,
                stop=self.plot,
                loggs=loggs,
                **self.kwargs
            ).compare
        )
        return super(ComparePipeline, self).transform(data, loggs)


class FitfunctionAssigner(TransformerBase):
    def __init__(self, fitf, plot=False):
        super(FitfunctionAssigner, self).__init__(plot)
        self.fitf = fitf

    def transform(self, histogram, loggs):
        if not self.fitf:
            return histogram
        histogram.fitfunc = self.fitf
        return histogram


class OutputFitter(TransformerBase):
    def __init__(self, options, plot=False):
        super(OutputFitter, self).__init__(plot)
        try:
            self.fitf = options.fitfunc
        except AttributeError:
            self.fitf = None

    def transform(self, histogram, loggs):
        if not self.fitf:
            return histogram

        histogram.Fit(self.fitf, "Rq")
        histogram.SetStats(True)
        st.fitstat_style()
        # Comparator(stop=self.plot).compare(histogram)
        ndf = self.fitf.GetNDF()
        chi2_ndf = self.fitf.GetChisquare() / ndf if ndf else 0.
        print "The chi2:", chi2_ndf
        print "The parameters", br.pars(self.fitf)
        Comparator().compare(histogram)
        return histogram


class OutputDecorator(TransformerBase):

    def __init__(self, histname, title=None, label=None, plot=False):
        super(OutputDecorator, self).__init__(plot)
        self.histname = histname
        self.title = title
        self.label = label

    def transform(self, data, loggs):
        new_name = "{}_{}".format(data.GetName(), self.histname)
        data.SetName(new_name)
        if self.title:
            data.SetTitle(self.title)

        if self.label:
            data.label = self.label
        loggs.update("decorated", [data])
        return data


class HistogramSelector(TransformerBase):

    def __init__(self, histname, plot=False):
        super(HistogramSelector, self).__init__(plot)
        self.histname = histname

    def transform(self, inputs, loggs):
        output = inputs._asdict()[self.histname]
        return output


class HistogramScaler(object):
    def __init__(self, factor=1., width=False):
        super(HistogramScaler, self).__init__()
        self.factor = factor
        self.width = width

    def transform(self, inputs, loggs):
        if self.width:
            br.scalew(inputs, self.factor)
        else:
            inputs.Scale(self.factor)
        return inputs


class FunctionTransformer(object):

    def __init__(self, func):
        super(FunctionTransformer, self).__init__()
        self.func = func

    def transform(self, inputs, loggs):
        output = self.func(inputs, loggs)
        return output


class Pipeline(object):

    def __init__(self, steps):
        super(Pipeline, self).__init__()
        self.steps = steps

    def transform(self, inputs, loggs):
        updated = inputs
        for name, step in self.steps:
            local_logs = AnalysisOutput(name)
            updated = step.transform(updated, local_logs)
            loggs.append(local_logs)
        return updated


class ParallelPipeline(object):

    def __init__(self, steps):
        super(ParallelPipeline, self).__init__()
        self.steps = steps

    def transform(self, inputs, loggs):
        assert len(inputs) == len(self.steps), \
            "Input shape doesn't match the shape" \
            " of estimators, got {0}, {1}".format(
            len(inputs),
            len(self.steps)
        )

        def tr(x, name, step, loggs):
            local_logs = AnalysisOutput(name)
            output = step.transform(x, local_logs)
            # print "Printing local logs", local_logs
            loggs.append(local_logs)
            return output, local_logs.mergelist()

        output_with_logs = [
            tr(inp, name, step, loggs)
            for inp, (name, step) in zip(inputs, self.steps)
        ]

        outputs, local_logs = zip(*output_with_logs)

        merged_loggs = AnalysisOutput(loggs.label)
        merged_loggs.pool = [
            MergedLogItem("merged", local)
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


class ReducePipelineLoggs(ReducePipeline):

    def transform(self, inputs, loggs):
        updated = self.parallel.transform(inputs, loggs)
        return self.function(updated, loggs)


class ReduceArgumentPipeline(object):

    def __init__(self, parallel, argument, function):
        super(ReduceArgumentPipeline, self).__init__()
        self.parallel = parallel
        self.argument = argument
        self.function = function

    def transform(self, inputs, loggs):
        argument_inp, inputs_inp = inputs
        argument = self.argument.transform(argument_inp, loggs)
        updated = self.parallel.transform(inputs_inp, loggs)
        return [self.function(o, argument) for o in updated]


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
        loggs.update("ratio_union", [[numerator, denominator]], mergable=True)
        return br.ratio(numerator, denominator, self.error)
