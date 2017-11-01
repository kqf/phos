#!/usr/bin/python

import ROOT
import json
from sutils import gcanvas, wait, adjust_canvas, ticks
from ptanalyzer import PtAnalyzer
from options import Options
from broot import BROOT as br


ROOT.TH1.AddDirectory(False)

class Spectrum(object):

    def __init__(self, lst, options = Options()):
        super(Spectrum, self).__init__()
        self.analyzer = PtAnalyzer(lst, options)
        self.opt = options.spectrum
        self.label = options.pt.label

    def _mass_ranges(self):
        quantities = self.analyzer.quantities(False)
        ranges = self._fit_ranges(quantities)
        return ranges

    def evaluate(self):
        ranges = self._mass_ranges()
        return self.analyzer.quantities(True, ranges)

    def _fit_quantity(self, quant, func, par, names, pref):
        fitquant = ROOT.TF1("fitquant" + pref, func)
        fitquant.SetLineColor(46)


        if not self.opt.dead:
            canvas = gcanvas(1./ 2., 1, True)
            adjust_canvas(canvas)
            ticks(canvas) 
            quant.Draw()

        fitquant.SetParameters(*par)
        fitquant.SetParNames(*names)

        # Doesn't fit and use default parameters for 
        # width/mass, therefore this will give correct estimation
        if not self.opt.fit_mass_width:
            [fitquant.FixParameter(i, p) for i, p in enumerate(par)]


        quant.Fit(fitquant, "q", "", *self.opt.fit_range)

        # print [fitquant.GetParameter(i) for i, p in enumerate(par)]
        quant.SetLineColor(37)
        wait(pref + "-paramerisation-" + self.label, self.opt.show_img, True)
        return fitquant

        
    def _fit_ranges(self, quantities):
        ROOT.gStyle.SetOptStat('')
        mass, sigma = quantities.mass, quantities.width

        fitsigma = self._fit_quantity(sigma, self.opt.width_func, self.opt.width_pars, self.opt.width_names, 'width')
        fitmass = self._fit_quantity(mass, self.opt.mass_func, self.opt.mass_pars, self.opt.mass_names, 'mass')

        mass_range = lambda pt: (fitmass.Eval(pt) - self.opt.nsigmas * fitsigma.Eval(pt),
                                 fitmass.Eval(pt) + self.opt.nsigmas * fitsigma.Eval(pt))

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 


class CompositeSpectrum(Spectrum):

    def __init__(self, lst, options = Options()):
        super(CompositeSpectrum, self).__init__(lst.keys()[0], options)
        self.spectrums = [Spectrum(l, Options(options.label, mode = 'd')) for l in lst]

        for est, rr in zip(self.spectrums, lst.values()):
            est.opt.fit_range = rr

    def evaluate(self):
        hists = [s.evaluate() for s in self.spectrums]
        ranges = [s.opt.fit_range for s in self.spectrums]
        
        # Transpose
        hists = zip(*hists)
        truncated = [br.sum_trimm(obs_pt, ranges) for obs_pt in hists]
        for h in truncated: 
            h.label = self.label 

        # Use the same container as normal analysis
        # 
        return self.analyzer.OutType(*truncated)

