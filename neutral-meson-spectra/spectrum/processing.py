#!/usr/bin/python

import ROOT
import sutils as su

from invariantmass import InvariantMass
from outputcreator import OutputCreator, SpectrumExtractor
import collections as coll
from ptplotter import PtPlotter
from mass import BackgroundEstimator, MixingBackgroundEstimator, SignalExtractor, SignalFitter, ZeroBinsCleaner


class DataSlicer(object):
    def __init__(self, options, all_options):
        super(DataSlicer, self).__init__()
        self.opt = options
        self.all_options = all_options

    def transform(self, inputs, loggs):
        intervals = zip(self.opt.ptedges[:-1], self.opt.ptedges[1:])
        assert len(intervals) == len(self.opt.rebins), \
            'Number of intervals is not equal to the number of rebin parameters'

        common_inputs = lambda x, y: InvariantMass(inputs, x, y, self.all_options)
        return map(common_inputs,
            intervals,
            self.opt.rebins
        )


class MassFitter(object):

    def __init__(self, options):
        super(MassFitter, self).__init__()
        self.opt = options

    def transform(self, masses, loggs):
        pipeline = self.pipeline(self.opt.use_mixed)

        for estimator in pipeline:
            output = map(
                estimator.transform, 
                masses
            )

            # TODO: Should I use this method or rely on invariant mass?
            # loggs.update(
            #     estimator.__class__.__name__,
            #     output,
            #     multirange=True
            # )
        return masses

    def pipeline(self, use_mixed):
        if not use_mixed:
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

    _output = 'mass', 'width'
    _titles = 'particle mass', 'particle width'
    def __init__(self, options):
        super(RangeEstimator, self).__init__()
        self.opt = options
        self.output = None

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract(
            self._output,
            masses
        )
        
        titles = {q: t for q, t in zip(self._output, self._titles)}

        self.output = OutputCreator.output(
           'MassWidthOutput',
            values, 
            self._output,
            InvariantMass.ptedges(masses),
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


        if not self.opt.dead:
            canvas = su.gcanvas(1./ 2., 1, True)
            su.adjust_canvas(canvas)
            su.ticks(canvas) 
            quant.Draw()

        fitquant.SetParameters(*par)
        fitquant.SetParNames(*names)

        # Doesn't fit and use default parameters for 
        # width/mass, therefore this will give correct estimation
        if not self.opt.fit_mass_width:
            [fitquant.FixParameter(i, p) for i, p in enumerate(par)]



        # print self.opt.fit_range
        quant.Fit(fitquant, "q", "", *self.opt.fit_range)

        # TODO: Now we mutate options. Should we do it in future?
        # Update the parameters
        for i in range(fitquant.GetNpar()):
            par[i] = fitquant.GetParameter(i)

        # print [fitquant.GetParameter(i) for i, p in enumerate(par)]
        quant.SetLineColor(37)

        # TODO: Move this to the output
        su.wait(pref + "-paramerisation-", self.opt.show_img, True)
        return fitquant

    def _fit_ranges(self, quantities, loggs):
        ROOT.gStyle.SetOptStat('')
        mass, sigma = quantities.mass, quantities.width

        massf = self.fit_mass(mass)
        sigmaf = self.fit_sigma(sigma)

        mass_range = lambda pt: (
            massf.Eval(pt) - self.opt.nsigmas * sigmaf.Eval(pt),
            massf.Eval(pt) + self.opt.nsigmas * sigmaf.Eval(pt)
        )

        loggs.update("range_estimator", [mass, sigma])

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
        
    def fit_mass(self, mass):
        return self._fit_quantity(mass,
            self.opt.mass_func,
            self.opt.mass_pars,
            self.opt.mass_names,
            'mass'
        ) 

    def fit_sigma(self, sigma):
        return self._fit_quantity(sigma, 
            self.opt.width_func, 
            self.opt.width_pars, 
            self.opt.width_names, 
            'width'
        )

        
class DataExtractor(object):

    def __init__(self, options):
        super(DataExtractor, self).__init__()
        self.opt = options

    def _decorate_hists(self, histograms, nevents):
        # Scale by the number of events 
        histograms.spectrum.Scale(1. / nevents)
        histograms.spectrum.logy = True
        histograms.npi0.logy = True
        return histograms 

    def transform(self, masses, loggs):
        values = SpectrumExtractor.extract(
            self.opt.output_order,
            masses
        )

        edges = InvariantMass.ptedges(masses)

        titles = {quant:
            self.opt.output[quant] % self.opt.particle 
            for quant in self.opt.output_order
        }

        # Create hitograms
        histos = OutputCreator.output(
           'SpectrumAnalysisOutput',
            values, 
            self.opt.output_order,
            edges,
            titles,
            loggs.label
        )


        # Decorate the histograms
        nevents = next(iter(masses)).mass.nevents
        decorated = self._decorate_hists(histos, nevents)

        loggs.update("invariant_masses", masses, multirange=True)
        loggs.update("analysis_output", decorated)
        return decorated 

