#!/usr/bin/python

import ROOT
import json
from sutils import gcanvas, wait, adjust_canvas, ticks
from kinematic import KinematicTransformer
from options import Options
from broot import BROOT as br


ROOT.TH1.AddDirectory(False)

class Analysis(object):

    def __init__(self, options = Options()):
        super(Analysis, self).__init__()
        self.options = options
        self.opt = options.spectrum

    def _mass_ranges(self, analyzer):
        quantities = analyzer.quantities(False)
        ranges = self._fit_ranges(quantities)
        return ranges

    def transform(self, data):
        self.label = data.label
        analyzer = KinematicTransformer(data, self.options)
        ranges = self._mass_ranges(analyzer)
        return analyzer.quantities(True, ranges)

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


        # print self.opt.fit_range
        quant.Fit(fitquant, "q", "", *self.opt.fit_range)

        # print [fitquant.GetParameter(i) for i, p in enumerate(par)]
        quant.SetLineColor(37)
        wait(pref + "-paramerisation-" + self.label, self.opt.show_img, True)
        return fitquant

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

    def _fit_ranges(self, quantities):
        ROOT.gStyle.SetOptStat('')
        mass, sigma = quantities.mass, quantities.width

        massf = self.fit_mass(mass)
        sigmaf = self.fit_sigma(sigma)

        mass_range = lambda pt: (massf.Eval(pt) - self.opt.nsigmas * sigmaf.Eval(pt),
                                 massf.Eval(pt) + self.opt.nsigmas * sigmaf.Eval(pt))

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
