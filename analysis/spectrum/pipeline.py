from __future__ import print_function

import array
from collections import defaultdict
from multimethod import multimethod
from flatten_dict import flatten, unflatten
import six
from tqdm import tqdm

import spectrum.sutils as st
import spectrum.broot as br
from spectrum.comparator import Comparator


class TransformerBase(object):

    def __init__(self, plot=True):
        super(TransformerBase, self).__init__()
        self.plot = plot

    def transform(self, inputs, loggs):
        return self.pipeline.transform(inputs, loggs)


class SingleHistReader(TransformerBase):
    def transform(self, data, loggs=None):
        return br.io.read(data.filename, data.listname, data.histname)


class AnalysisDataReader(TransformerBase):
    def _events(self, filename, listname):
        return br.io.read(
            filename,
            listname,
            "EventCounter").GetBinContent(2)

    def transform(self, data, loggs):
        hists = br.io.read_multiple(
            data.filename,
            data.listname,
            data.histnames
        )
        for h in hists:
            br.set_nevents(
                h, data.n_events or self._events(data.filename, data.listname))
        return hists, data.pt_range


class ComparePipeline(TransformerBase):

    def __init__(self, estimators, plot=False, **kwargs):
        super(ComparePipeline, self).__init__(plot)
        labels = list(zip(*estimators))[0]
        self.pipeline = ReducePipeline(
            ParallelPipeline(estimators),
            Comparator(labels=labels, stop=plot, **kwargs).compare
        )


class RebinTransformer(TransformerBase):
    def __init__(self, normalized, edges=None):
        self.normalized = normalized
        self.edges = edges

    @staticmethod
    def scale_bin_width(hist, aggregated_widths, normalized):
        name = "{}_width".format(hist.GetName())
        hist = hist.Clone(name)
        for i, width in zip(br.hrange(hist), aggregated_widths):
            hist.SetBinContent(i, hist.GetBinContent(i) / width)
            hist.SetBinError(i, hist.GetBinError(i) / width)
        return hist

    @staticmethod
    def meregd_bins(newh, oldh, normalized):
        new = br.edges(newh)

        def nbins(a, b):
            return [oldh.GetBinWidth(i)
                    for i in br.hrange(oldh) if a < oldh.GetBinCenter(i) < b]

        func = len if normalized else sum
        widths = [func(nbins(*edge)) for edge in zip(new[:-1], new[1:])]
        return widths

    @multimethod
    def transform(self, hist, loggs):
        if self.edges is None:
            return hist

        nbins = len(self.edges) - 1
        edges = array.array('d', self.edges)
        rebinned = hist.Rebin(nbins, hist.GetName(), edges)
        rebinned.SetName("{}_rebinned".format(hist.GetName()))

        rebinned = self.scale_bin_width(
            rebinned,
            self.meregd_bins(rebinned, hist, self.normalized),
            normalized=self.normalized)

        return rebinned

    @transform.register(TransformerBase, br.PhysicsHistogram)
    def _(self, hist, loggs):
        result = br.PhysicsHistogram(
            self.transform(hist.tot, loggs),
            self.transform(hist.stat, loggs),
            self.transform(hist.syst, loggs),
        )
        return result


class FitfunctionAssigner(TransformerBase):
    def __init__(self, fitfunc, plot=False):
        super(FitfunctionAssigner, self).__init__(plot)
        self.fitfunc = fitfunc

    def transform(self, histogram, loggs):
        if not self.fitfunc:
            return histogram
        histogram.fitfunc = self.fitfunc
        return histogram


class HistogramFitter(TransformerBase):
    def __init__(self, fitfunc, plot=False):
        super(HistogramFitter, self).__init__(plot)
        self.fitfunc = fitfunc

    def transform(self, histogram, loggs):
        if not self.fitfunc:
            return histogram

        histogram.Fit(self.fitfunc, "Rq")
        histogram.SetStats(True)
        st.fitstat_style()
        ndf = self.fitfunc.GetNDF()
        chi2_ndf = self.fitfunc.GetChisquare() / ndf if ndf else 0.
        print("The chi2:", chi2_ndf)
        print("The parameters", br.pars(self.fitfunc))
        Comparator().compare(histogram)
        return histogram


class DataFitter(TransformerBase):
    def __init__(self, fitf, xmin=None, xmax=None):
        self.fitf = fitf
        self.xmin = xmin
        self.xmax = xmax

    def transform(self, x, loggs):
        if self.fitf is None:
            x.fitf = None
            return x
        fitf = self.fitf.Clone()
        fitf.SetRange(
            self.xmin or x.GetXaxis().GetXmin(),
            self.xmax or x.GetXaxis().GetXmax(),
        )
        x.Fit(fitf, "QR")
        x.fitf = fitf
        return x


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


class FunctionTransformer(TransformerBase):

    def __init__(self, func, no_loggs=False, **kwargs):
        super(FunctionTransformer, self).__init__()
        self.func = func
        self.no_loggs = no_loggs
        self.kwargs = kwargs

    def transform(self, inputs, loggs):
        if not self.no_loggs:
            return self.func(inputs, loggs=loggs, **self.kwargs)
        return self.func(inputs, **self.kwargs)


class Pipeline(object):
    _output = "output"

    def __init__(self, steps, disable=True):
        super(Pipeline, self).__init__()
        self.steps = steps
        self.disable = disable

    def transform(self, inputs, loggs):
        updated = inputs
        for name, step in tqdm(self.steps, disable=self.disable):
            local_logs = {}
            updated = step.transform(updated, local_logs)
            if self._output not in local_logs:
                local_logs[self._output] = updated
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
        for path, value in six.iteritems(flat):
            output[path].append((label, value))
    # Merged item should have at least len 2, otherwise it's useless
    filtered = {k: v for k, v in six.iteritems(output) if len(v) > 1}
    return unflatten(filtered)


class ParallelPipeline(object):

    def __init__(self, steps, disable=True):
        super(ParallelPipeline, self).__init__()
        self.steps = steps
        self.disable = disable

    def transform(self, inputs, loggs):
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
            for inp, (name, step) in tqdm(list(zip(inputs, self.steps)),
                                          disable=self.disable)
        ]
        loggs.update({"steps": steps_loggs})

        outputs, local_logs = list(zip(*output_with_logs))
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
        self.parallel = parallel[1]
        self.argument = argument[1]

        self.parallel_name = parallel[0]
        self.argument_name = argument[0]

        self.function = function

    def transform(self, inputs, loggs):
        argument_inp, inputs_inp = inputs

        local_logs = {}
        argument = self.argument.transform(argument_inp, local_logs)
        loggs[self.argument_name] = local_logs

        local_logs = {}
        updated = self.parallel.transform(inputs_inp, local_logs)
        loggs[self.parallel_name] = local_logs

        return [self.function(o, argument, loggs=loggs) for o in updated]
