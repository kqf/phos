#!/usr/bin/python

import ROOT

from invariantmass import InvariantMass, RawMass
from outputcreator import analysis_output, SpectrumExtractor

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
            return RawMass(input_data, x, y)

        return map(common_inputs,
                   intervals,
                   self.opt.rebins
                   )


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

    _quantities = "mass", "width"
    _output = "fit_mass", "fit_width"
    _titles = (
        "Parametrized {} mass position; p_{T}, GeV/c; m, GeV",
        "Parametrized {} peak width; p_{T}, GeV/c; #sigma, GeV",
    )

    def __init__(self, options):
        super(RangeEstimator, self).__init__()
        self.opt = options
        self.output = None

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract(
            self._quantities,
            masses
        )

        titles = {q:
                  t.format(self.opt.particle, T="{T}")
                  for q, t in zip(self._output, self._titles)}

        self.output = analysis_output(
            "MassWidthOutput",
            values,
            self._output,
            self.opt.ptrange,
            RawMass.ptedges(masses),
            titles,
            loggs.label
        )

        ranges = self._fit_ranges(self.output, loggs)
        for mass, region in zip(masses, ranges):
            mass.integration_region = region

        return masses

    def _fit_quantity(self, quant, func, par, names, pref):
        fitquant = ROOT.TF1("fitquant" + pref, func)
        fitquant.SetLineColor(46)

        fitquant.SetParameters(*par)
        fitquant.SetParNames(*names)

        # Doesn't fit and use default parameters for
        # width/mass, therefore this will give correct estimation
        if not self.opt.fit_mass_width:
            [fitquant.FixParameter(i, p) for i, p in enumerate(par)]

        # fitquant.FixParameter(0, par[0])
        # fitquant.FixParameter(0, )

        quant.Fit(fitquant, "q")
        quant.GetListOfFunctions().Add(fitquant)

        # TODO: Now we mutate options. Should we do it in future?
        # Update the parameters
        for i in range(fitquant.GetNpar()):
            par[i] = fitquant.GetParameter(i)

        ndf = fitquant.GetNDF()
        chi2_ndf = fitquant.GetChisquare() / ndf if ndf else 0.
        # print chi2_ndf, self.opt.fit_range, par
        quant.SetTitle(
            quant.GetTitle() + ", #chi^{2}/ndf" + " = {chi2:0.4g}".format(
                chi2=chi2_ndf
            )
        )

        # print [fitquant.GetParameter(i) for i, p in enumerate(par)]
        quant.SetLineColor(37)
        return fitquant

    def _fit_ranges(self, quantities, loggs):
        ROOT.gStyle.SetOptStat("")
        mass, sigma = quantities.fit_mass, quantities.fit_width

        massf = self.fit_mass(mass)
        sigmaf = self.fit_sigma(sigma)

        def mass_range(pt):
            return (
                massf.Eval(pt) - self.opt.nsigmas * sigmaf.Eval(pt),
                massf.Eval(pt) + self.opt.nsigmas * sigmaf.Eval(pt)
            )

        loggs.update("range_estimator", [mass, sigma], mergable=True)

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values)

    def fit_mass(self, mass):
        return self._fit_quantity(mass,
                                  self.opt.mass_func,
                                  self.opt.mass_pars,
                                  self.opt.mass_names,
                                  "mass"
                                  )

    def fit_sigma(self, sigma):
        return self._fit_quantity(sigma,
                                  self.opt.width_func,
                                  self.opt.width_pars,
                                  self.opt.width_names,
                                  "width"
                                  )


class DataExtractor(object):

    def __init__(self, options):
        super(DataExtractor, self).__init__()
        self.opt = options

    def _decorate_hists(self, histograms, nevents):
        # Scale by the number of events
        if self.opt.scalew_spectrum:
            br.scalew(histograms.spectrum)
            br.scalew(histograms.nmesons)

        histograms.spectrum.Scale(1. / nevents)
        histograms.spectrum.logy = True
        histograms.nmesons.logy = True
        return histograms

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract(self.opt.output_order, masses)

        edges = RawMass.ptedges(masses)
        histos = analysis_output(
            "SpectrumAnalysisOutput",
            values,
            self.opt.output_order,
            self.opt.ptrange,
            edges,
            self.opt.output,
            loggs.label
        )

        # Decorate the histograms
        try:
            nevents = next(iter(masses)).mass.nevents
        except AttributeError:
            nevents = 1

        decorated = self._decorate_hists(histos, nevents)
        loggs.update("invariant_masses", masses, multirange=True)
        loggs.update("analysis_output", decorated, mergable=True)
        return decorated
