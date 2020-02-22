from __future__ import print_function
import ROOT
import numpy as np
import pandas as pd
import collections


import humanize
import spectrum.broot as br
from spectrum.constants import PAVE_PREFIX

from spectrum.pipeline import Pipeline, TransformerBase
from spectrum.parametrisation import parametrisation as pr

from spectrum.ptplotter import MulipleOutput
from spectrum.mass import BackgroundEstimator, MixingBackgroundEstimator
from spectrum.mass import SignalExtractor, SignalFitter, ZeroBinsCleaner
from spectrum.mass import SignalFitExtractor, FitQualityExtractor
from spectrum.mass import MassTransformer


class DataPreparator(TransformerBase):
    def __init__(self, options):
        super(DataPreparator, self).__init__()
        self.opt = options
        self.pipeline = Pipeline([
            ("slicer", DataPreprocessor(self.opt))
        ])


class DataPreprocessor(object):
    reactions = {
        "#pi^{0}": "#pi^{0} #rightarrow #gamma #gamma",
        "#eta": "#eta #rightarrow #gamma #gamma",
        "electrons": "#it{e}^{#pm}",
    }

    xaxis = {
        "#pi^{0}": "#it{M}_{#gamma#gamma} (GeV/#it{c}^{2})",
        "#eta": "#it{M}_{#gamma#gamma} (GeV/#it{c}^{2})",
        "electrons": "#it{E}/#it{p} ratio",
    }

    def __init__(self, options):
        super(DataPreprocessor, self).__init__()
        self.opt = options
        self.particle = self.opt.particle

    def transform(self, inputs, loggs):
        histograms, pt_range = inputs
        if len(histograms) == 1:
            histograms = histograms + [None]
        same, mixed = histograms

        intervals = list(zip(self.opt.ptedges[:-1], self.opt.ptedges[1:]))
        assert len(intervals) == len(self.opt.rebins), \
            "Number of intervals is not equal " \
            "to the number of rebin parameters" \
            "edges = {} vs rebins = {}".format(
                len(intervals),
                len(self.opt.rebins)
        )

        label = "{:.4g} < #it{{p}}_{{T}} < {:.4g} GeV/#it{{c}}"
        pt_labels = [label.format(*i) for i in intervals]

        df = pd.DataFrame({
            "intervals": intervals,
            "pt_interval": [pt_range] * len(intervals),
            "pt_range": intervals,
            "pt_edges": [self.opt.ptedges] * len(intervals),
            "pt_label": pt_labels,
        })
        df["nevents"] = same.nevents
        args = list(zip(intervals, self.opt.rebins, pt_labels))
        df["measured"] = [self.mass(same, *a) for a in args]
        if mixed is not None:
            df["background"] = [self.mass(mixed, *a) for a in args]
        return df

    def mass(self, hist, pt_range, nrebin, pt_label):
        mass = br.project_range(hist, *pt_range)
        mass.nevents = hist.nevents
        title = (
            "{prefix} "
            "| {reaction} "
            "| {pt} "
            "| #it{{N}}_{{events}} = {events}"
        ).format(
            prefix=PAVE_PREFIX,
            reaction=self.reactions[self.particle],
            pt=pt_label,
            events=humanize.intword(mass.nevents)
        )
        mass.SetTitle(title)
        mass.GetXaxis().SetTitle(self.xaxis[self.particle])
        mass.GetYaxis().SetTitle("counts")
        mass.SetLineColor(ROOT.kRed + 1)

        if not mass.GetSumw2N():
            mass.Sumw2()

        if nrebin:
            mass.Rebin(nrebin)
        return mass


class InvariantMassExtractor(object):
    def __init__(self, options):
        super(InvariantMassExtractor, self).__init__()
        self.opt = options

    def transform(self, rmasses, loggs):
        nbins = len(rmasses)
        rmasses["tol"] = [self.opt.tol] * nbins
        rmasses["fit_range"] = [self.opt.signal.fit_range] * nbins
        rmasses["measured_fitter"] = [pr(self.opt.background)] * nbins
        rmasses["signal_fitter"] = [pr(self.opt.signal)] * nbins
        return rmasses


class MassFitPtLogger(TransformerBase):
    def transform(self, masses, loggs):
        params = masses["signalf"].apply(
            lambda f: {
                f.GetParName(i): f.GetParameter(i) for i in range(f.GetNpar())}
        )
        params = pd.DataFrame(params.to_dict()).T

        out = []
        for col in params:
            title = "Signal parametrisation parameter {}".format(col)
            hist = br.table2hist(
                col,
                title,
                params[col],
                np.zeros_like(params[col]),
                masses["pt_edges"][0],
            )
            out.append(hist)
        loggs.update({"output": tuple(out)})
        return masses


class MassFitter(TransformerBase):

    def __init__(self, use_mixed):
        super(MassFitter, self).__init__()
        self.pipeline = Pipeline(self.background(use_mixed) + [
            ("signal", SignalExtractor()),
            ("signal-fit", SignalFitter()),
            ("extract-signal", SignalFitExtractor(in_cols=["signalf"])),
            ("extract-measured", SignalFitExtractor(in_cols=["measuredf"],
                                                    prefix="background_")),
            ("quality-signal", FitQualityExtractor(in_cols=["signalf"])),
            ("quality-measured", FitQualityExtractor(in_cols=["measuredf"],
                                                     prefix="background_")),
            ("signal-fit-log", MassFitPtLogger()),
        ])

    @staticmethod
    def background(use_mixed):
        if not use_mixed:
            return [("background", BackgroundEstimator())]

        steps = [
            ("mixing", MixingBackgroundEstimator()),
            ("background", ZeroBinsCleaner())
        ]
        return steps


class PtFitter(object):

    def __init__(self, col, err, out_col, options):
        super(PtFitter, self).__init__()
        self.col = col
        self.err = err
        self.out_col = out_col
        self.opt = options

    def transform(self, masses, loggs):
        target_quantity = br.table2hist(
            self.out_col,
            self.opt.title.format(self.opt.particle),
            masses[self.col],
            masses[self.err],
            masses["pt_edges"][0],
            roi=masses["pt_interval"].values[0],
        )
        fitf = self._fit(target_quantity, loggs)
        masses[self.out_col] = [fitf] * len(masses)
        return masses

    def _fit(self, hist, loggs={}):
        fitquant = ROOT.TF1("fit_{}".format(self.opt.quantity), self.opt.func)
        fitquant.SetParameters(*self.opt.pars)
        fitquant.SetParNames(*self.opt.names)
        fitquant.SetLineColor(46)

        # Doesn't fit and use default parameters for
        # width/mass, therefore this will give correct estimation
        if not self.opt.fit:
            [fitquant.FixParameter(i, p) for i, p in enumerate(self.opt.pars)]
        # fitquant.FixParameter(0, par[0])
        # fitquant.FixParameter(0, )

        hist.Fit(fitquant, "qww")
        hist.GetListOfFunctions().Add(fitquant)

        # TODO: Now we mutate options. Should we do it in future?
        # Update the parameters
        for i in range(fitquant.GetNpar()):
            self.opt.pars[i] = fitquant.GetParameter(i)

        title = "{}, #chi^{{2}}/ndf = {:0.4g}"
        hist.SetTitle(title.format(hist.GetTitle(), br.chi2ndff(fitquant)))
        hist.SetLineColor(37)
        loggs.update({"output": hist})
        return fitquant


class RangeEstimator(MassTransformer):
    in_cols = ["pposition_pt_f", "pwidth_pt_f", "intervals"]
    out_cols = "integration_region"

    def __init__(self, options):
        super(RangeEstimator, self).__init__()
        self.nsigmas = options.nsigmas

    def apply(self, position, width, intervals):
        pt = intervals[0] + (intervals[1] - intervals[0]) / 2
        integration_region = (
            position.Eval(pt) - self.nsigmas * width.Eval(pt),
            position.Eval(pt) + self.nsigmas * width.Eval(pt)
        )
        return integration_region


class PeakAreaEstimator(MassTransformer):
    in_cols = ["signal", "integration_region"]
    out_cols = ["nmesons", "nmesons_error"]
    result_type = "expand"

    def apply(self, signal, integration_region):
        area, areae = br.area_and_error(signal, *integration_region)
        return area, areae


class SpectrumEstimator(object):
    def transform(self, masses, loggs):
        bin_widths = masses["intervals"].str[1] - masses["intervals"].str[0]
        masses["nmesons"] = masses["nmesons"] / bin_widths
        masses["spectrum"] = masses["nmesons"] / masses["nevents"]

        masses["nmesons_error"] = masses["nmesons_error"] / bin_widths
        masses["spectrum_error"] = masses["nmesons_error"] / masses["nevents"]
        return masses


class PeakPropertiesEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(PeakPropertiesEstimator, self).__init__(plot=plot)
        self.pipeline = Pipeline([
            ("peak-position", PtFitter(
                col="mass",
                err="mass_error",
                out_col="pposition_pt_f",
                options=options.mass)),
            ("peak-width", PtFitter(
                col="width",
                err="width_error",
                out_col="pwidth_pt_f",
                options=options.width)),
            ("ranges", RangeEstimator(options)),
            ("area", PeakAreaEstimator()),
            ("spectrum", SpectrumEstimator()),
        ])


class InvariantMassPlotter(TransformerBase):
    def transform(self, masses, loggs):
        loggs.update({
            "output":
            MulipleOutput(masses.to_dict(orient="records"))
        })
        return masses


class DataExtractor(object):

    def __init__(self, options):
        super(DataExtractor, self).__init__()
        self.opt = options
        self.otype = collections.namedtuple(
            "SpectrumAnalysisOutput", self.opt.output_order)

    def transform(self, masses, loggs):
        data = []
        for o in self.otype._fields:
            data.append(
                br.table2hist(
                    o,
                    self.opt.output[o],
                    masses[o],
                    masses["{}_error".format(o)],
                    masses["pt_edges"][0])
            )

        return self.otype(*data)
