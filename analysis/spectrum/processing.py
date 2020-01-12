from __future__ import print_function
import ROOT
import pandas as pd

from spectrum.invariantmass import InvariantMass, RawMass, masses2edges
from spectrum.outputcreator import analysis_output, SpectrumExtractor
from spectrum.outputcreator import table2hist
from spectrum.pipeline import Pipeline

from spectrum.ptplotter import MulipleOutput
from spectrum.mass import BackgroundEstimator, MixingBackgroundEstimator
from spectrum.mass import SignalExtractor, SignalFitter, ZeroBinsCleaner
import spectrum.broot as br


class DataSlicer(object):
    def __init__(self, options):
        super(DataSlicer, self).__init__()
        self.opt = options

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

        def common_inputs(x, y):
            return RawMass(x, y, self.opt.particle, pt_interval=pt_range)

        readers = list(map(common_inputs, intervals, self.opt.rebins))
        return pd.DataFrame(
            {
                "intervals": intervals,
                "pt_interval": [pt_range] * len(intervals),
                "pt_edges": [self.opt.ptedges] * len(intervals),
                "raw": readers,
                "measured": [r.transform(same) for r in readers],
                "background": [r.transform(mixed) for r in readers],
                "nevents": [same.nevents] * len(intervals)
            }
        )


class InvariantMassExtractor(object):

    def __init__(self, options):
        super(InvariantMassExtractor, self).__init__()
        self.opt = options

    def transform(self, rmasses, loggs):
        rmasses["invmasses"] = rmasses["raw"].apply(
            lambda x: InvariantMass(x, self.opt))
        rmasses["pt_range"] = rmasses["invmasses"].apply(lambda x: x.pt_range)
        rmasses["pt_label"] = rmasses["invmasses"].apply(lambda x: x.pt_label)
        return rmasses


class MassFitter(object):

    def __init__(self, use_mixed):
        super(MassFitter, self).__init__()
        self.use_mixed = use_mixed

    def transform(self, masses, loggs):
        pipeline = self._pipeline()

        for estimator in pipeline:
            estimator.transform(masses, loggs)

        params = masses["signal_fitf"].apply(
            lambda f: {
                f.GetParName(i): f.GetParameter(i) for i in range(f.GetNpar())}
        )

        params = pd.DataFrame(params.to_dict()).T

        out = []
        for col in params:
            title = "Signal parametrisation parameter {}".format(col)
            hist = table2hist(col, title, params[col], masses["pt_edges"][0])
            out.append(hist)
        loggs.update({"output": tuple(out)})
        return masses

    def _pipeline(self):
        if not self.use_mixed:
            return [
                BackgroundEstimator(),
                SignalExtractor(),
                SignalFitter()
            ]
        return [
            MixingBackgroundEstimator(),
            ZeroBinsCleaner(),
            SignalExtractor(),
            SignalFitter()
        ]


class RangeEstimator(object):
    def __init__(self, options):
        super(RangeEstimator, self).__init__()
        self.mass = Pipeline([("mass", PtFitter(options.mass))])
        self.width = Pipeline([("width", PtFitter(options.width))])
        self.nsigmas = options.nsigmas

    def transform(self, masses, loggs):
        ranges = self._fit(masses, loggs)
        for mass, region in zip(masses["invmasses"], ranges):
            mass.integration_region = region
        return masses

    def _fit(self, masses, loggs):
        ROOT.gStyle.SetOptStat("")
        mass = self.mass.transform(masses, loggs)
        sigma = self.width.transform(masses, loggs)

        massf = mass.fitf
        sigmaf = sigma.fitf

        def mass_range(pt):
            return (
                massf.Eval(pt) - self.nsigmas * sigmaf.Eval(pt),
                massf.Eval(pt) + self.nsigmas * sigmaf.Eval(pt)
            )

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values)


class PtFitter(object):

    def __init__(self, options):
        super(PtFitter, self).__init__()
        self.opt = options

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract([self.opt.quantity],
                                           masses["invmasses"])

        title = self.opt.title.format(self.opt.particle)
        target_quantity = analysis_output(
            self.opt.quantity,
            values,
            [self.opt.quantity],
            masses["pt_interval"].values[0],
            masses2edges(masses["invmasses"]),
            {self.opt.quantity: title},
        )
        return self._fit(target_quantity[0])

    def _fit(self, hist):
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

        ndf = fitquant.GetNDF()
        chi2_ndf = fitquant.GetChisquare() / ndf if ndf else 0.
        # print(chi2_ndf, self.opt.opt.fit_range, par)
        hist.SetTitle(
            hist.GetTitle() + ", #chi^{2}/ndf" + " = {chi2:0.4g}".format(
                chi2=chi2_ndf
            )
        )
        # print([fitquant.GetParameter(i) for i, p in enumerate(par)])
        hist.SetLineColor(37)
        hist.fitf = fitquant
        return hist


class DataExtractor(object):

    def __init__(self, options):
        super(DataExtractor, self).__init__()
        self.opt = options

    def _decorate_hists(self, histograms, nevents):
        # Scale by the number of events
        if self.opt.scalew_spectrum:
            br.scalewidth(histograms.spectrum)
            br.scalewidth(histograms.nmesons)

        histograms.spectrum.Scale(1. / nevents)
        histograms.spectrum.logy = True
        histograms.nmesons.logy = True
        return histograms

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract(self.opt.output_order,
                                           masses["invmasses"])

        # pt = masses["pt_edges"][0]
        # for o in self.opt.output_order:
        #     print(table2hist(o, self.opt.output[o], masses[o], masses[o], pt))

        histos = analysis_output(
            "SpectrumAnalysisOutput",
            values,
            self.opt.output_order,
            masses["pt_interval"].values[0],
            masses2edges(masses["invmasses"]),
            self.opt.output,
        )

        nevents = next(iter(masses["nevents"]))
        decorated = self._decorate_hists(histos, nevents)
        loggs.update({"invariant_masses": MulipleOutput(masses["invmasses"])})
        return decorated
