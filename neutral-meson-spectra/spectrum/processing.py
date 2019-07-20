from __future__ import print_function
import ROOT

from invariantmass import InvariantMass, RawMass, masses2edges
from outputcreator import analysis_output, SpectrumExtractor

from ptplotter import MulipleOutput
from mass import BackgroundEstimator, MixingBackgroundEstimator
from mass import SignalExtractor, SignalFitter, ZeroBinsCleaner
from broot import BROOT as br


class DataSlicer(object):
    def __init__(self, options):
        super(DataSlicer, self).__init__()
        self.opt = options

    def transform(self, inputs, loggs):
        input_data = inputs.transform()

        intervals = zip(self.opt.ptedges[:-1], self.opt.ptedges[1:])
        assert len(intervals) == len(self.opt.rebins), \
            "Number of intervals is not equal " \
            "to the number of rebin parameters" \
            "edges = {} vs rebins = {}".format(
                len(intervals),
                len(self.opt.rebins)
        )

        def common_inputs(x, y):
            return RawMass(input_data, x, y, pt_interval=inputs.pt_range)

        return map(common_inputs, intervals, self.opt.rebins)


class InvariantMassExtractor(object):

    def __init__(self, options):
        super(InvariantMassExtractor, self).__init__()
        self.opt = options

    def transform(self, rmasses, loggs):
        return map(lambda x: InvariantMass(x, self.opt), rmasses)


class MassFitter(object):

    def __init__(self, use_mixed):
        super(MassFitter, self).__init__()
        self.use_mixed = use_mixed

    def transform(self, masses, loggs):
        pipeline = self._pipeline()

        for estimator in pipeline:
            map(estimator.transform, masses)

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

    _titles = (
        "Parametrized {} mass position; p_{{T}}, GeV/c; m, GeV",
        "Parametrized {} peak width; p_{{T}}, GeV/c; #sigma, GeV",
    )

    def __init__(self, options):
        super(RangeEstimator, self).__init__()
        self.opt = options
        self.output = None
        self.width_pipeline = PtFitter(options,
                                       "width",
                                       self._titles[1],
                                       self.opt.width_func,
                                       self.opt.width_pars,
                                       self.opt.width_names,
                                       )

        self.mass_pipeline = PtFitter(options,
                                      "mass",
                                      self._titles[0],
                                      self.opt.mass_func,
                                      self.opt.mass_pars,
                                      self.opt.mass_names,
                                      )

    def transform(self, masses, loggs):
        ranges = self._fit(masses, loggs)
        for mass, region in zip(masses, ranges):
            mass.integration_region = region
        return masses

    def _fit(self, masses, loggs):
        ROOT.gStyle.SetOptStat("")
        mass = self.mass_pipeline.transform(masses, loggs)
        sigma = self.width_pipeline.transform(masses, loggs)

        massf = mass.fitf
        sigmaf = sigma.fitf

        def mass_range(pt):
            return (
                massf.Eval(pt) - self.opt.nsigmas * sigmaf.Eval(pt),
                massf.Eval(pt) + self.opt.nsigmas * sigmaf.Eval(pt)
            )

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values)


class PtFitter(object):

    def __init__(self, options, quantity, title, func, par, names):
        super(PtFitter, self).__init__()
        self.opt = options
        self.quantity = quantity
        self.title = title
        self.func = func
        self.par = par
        self.names = names

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract([self.quantity], masses)
        title = self.title.format(self.opt.particle)
        target_quantity = analysis_output(
            self.quantity,
            values,
            [self.quantity],
            masses[0].pt_interval,
            masses2edges(masses),
            {self.quantity: title},
            ""
        )
        return self._fit(target_quantity[0])

    def _fit(self, hist):
        fitquant = ROOT.TF1("fit_{}".format(self.quantity), self.func)
        fitquant.SetParameters(*self.par)
        fitquant.SetParNames(*self.names)
        fitquant.SetLineColor(46)

        # Doesn't fit and use default parameters for
        # width/mass, therefore this will give correct estimation
        if not self.opt.fit_mass_width:
            print("Using pars", self.mass_pars)
            [fitquant.FixParameter(i, p) for i, p in enumerate(self.par)]
        # fitquant.FixParameter(0, par[0])
        # fitquant.FixParameter(0, )

        hist.Fit(fitquant, "q")
        hist.GetListOfFunctions().Add(fitquant)

        # TODO: Now we mutate options. Should we do it in future?
        # Update the parameters
        for i in range(fitquant.GetNpar()):
            self.par[i] = fitquant.GetParameter(i)

        ndf = fitquant.GetNDF()
        chi2_ndf = fitquant.GetChisquare() / ndf if ndf else 0.
        # print(chi2_ndf, self.opt.fit_range, par)
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
        values = SpectrumExtractor.extract(self.opt.output_order, masses)

        histos = analysis_output(
            "SpectrumAnalysisOutput",
            values,
            self.opt.output_order,
            masses[0].pt_interval,
            masses2edges(masses),
            self.opt.output,
            ""
        )

        # Decorate the histograms
        try:
            nevents = next(iter(masses)).mass.nevents
        except AttributeError:
            nevents = 1

        decorated = self._decorate_hists(histos, nevents)
        loggs.update({"invariant_masses": MulipleOutput(masses)})
        # TODO: Don't save here, add another step to the pipeline
        loggs.update({"analysis_output": decorated._asdict()})
        return decorated
