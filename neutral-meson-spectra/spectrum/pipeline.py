from __future__ import print_function

import array
from collections import defaultdict

from tqdm import tqdm
from flatten_dict import flatten, unflatten

import sutils as st
from broot import BROOT as br
from comparator import Comparator


class TransformerBase(object):

    def __init__(self, plot=True):
        super(TransformerBase, self).__init__()
        self.plot = plot

    def transform(self, inputs, loggs):
        output = self.pipeline.transform(inputs, loggs)
        if output:
            loggs.update({'output': output})
        return output


class ComparePipeline(TransformerBase):

    def __init__(self, estimators, plot=False, **kwargs):
        super(ComparePipeline, self).__init__(plot)
        labels = zip(*estimators)[0]
        self.pipeline = ReducePipeline(
            ParallelPipeline(estimators),
            Comparator(labels=labels, stop=plot, **kwargs).compare
        )


class RebinTransformer(TransformerBase):
    def __init__(self, edges, plot=False, width=True):
        super(RebinTransformer, self).__init__(plot)
        self.edges = array.array('d', edges)
        self.width = width

    def transform(self, data, loggs):
        newname = "{0}_rebinned".format(data.GetName())
        rebinned = data.Rebin(len(self.edges) - 1, newname, self.edges)
        if self.width:
            rebinned.Scale(data.GetBinWidth(1), "width")
            # br.scalewidth(rebinned)
        loggs.update({"rebinned": rebinned})
        return rebinned


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
        print("The chi2:", chi2_ndf)
        print("The parameters", br.pars(self.fitf))
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
        loggs.update({"decorated": data})
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
            # br.scalew(inputs, self.factor)
            raise IOError("Don't use this option")
        else:
            inputs.Scale(self.factor)
        return inputs


class FunctionTransformer(object):

    def __init__(self, func):
        super(FunctionTransformer, self).__init__()
        self.func = func

    def transform(self, inputs, loggs):
        output = self.func(inputs, loggs=loggs)
        return output


class Pipeline(object):

    def __init__(self, steps, disable=True):
        super(Pipeline, self).__init__()
        self.steps = steps
        self.disable = disable

    def transform(self, inputs, loggs):
        updated = inputs
        for name, step in tqdm(self.steps, disable=self.disable):
            local_logs = {}
            updated = step.transform(updated, local_logs)
            loggs[name] = local_logs
        return updated


def merge(data):
    """
    input:
         data = list of (str, dict)
    output:
         dict with the same structure as input dict
    """
    output = defaultdict(list)
    for label, ddict in data:
        flat = flatten(ddict)
        for path, value in flat.iteritems():
            output[path].append((label, value))
    # Merged item should have at least len 2, otherwise it's useless
    filtered = {k: v for k, v in output.iteritems() if len(v) > 1}
    return unflatten(filtered)


class ParallelPipeline(object):

    def __init__(self, steps):
        super(ParallelPipeline, self).__init__()
        self.steps = steps

    def transform(self, inputs, loggs):
        # import ipdb; ipdb.set_trace()
        assert len(inputs) == len(self.steps), \
            "Input shape doesn't match the shape" \
            " of estimators, got {0}, {1}".format(
            len(inputs),
            len(self.steps)
        )

        def tr(x, name, step, loggs):
            local_logs = {}
            output = step.transform(x, local_logs)
            loggs.update({name: local_logs})
            return output, (name, local_logs)

        steps_loggs = {}
        output_with_logs = [
            tr(inp, name, step, steps_loggs)
            for inp, (name, step) in zip(inputs, self.steps)
        ]
        loggs.update({"steps": steps_loggs})

        outputs, local_logs = zip(*output_with_logs)
        loggs.update({"merged": merge(local_logs)})
        return outputs


class ReducePipeline(object):

    def __init__(self, parallel, function):
        super(ReducePipeline, self).__init__()
        self.parallel = parallel
        self.function = function

    def transform(self, inputs, loggs):
        updated = self.parallel.transform(inputs, loggs)
        return self.function(updated, loggs=loggs)


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
        return [self.function(o, argument, loggs=loggs) for o in updated]
