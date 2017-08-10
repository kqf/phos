#!/usr/bin/python

import ROOT
import json
from sutils import get_canvas, wait, adjust_canvas, ticks
from ptanalyzer import PtAnalyzer
from options import Options


ROOT.TH1.AddDirectory(False)

class Spectrum(object):

    def __init__(self, lst, options = Options()):
        super(Spectrum, self).__init__()
        soptions = options.spectrum
        self.nsigmas = soptions.nsigmas
        self.analyzer = PtAnalyzer(lst, options)
        self.fit = soptions.fit_mass_width


        self.canvas = soptions.conf['canvas']
        config = soptions.conf[options.particle]

        # Width parametrizatin
        self.width_func  = config['width_func']
        self.width_pars  = config['width_pars']
        self.width_names = config['width_names']

        # Mass parametrizatin
        self.mass_func   = config['mass_func']
        self.mass_pars   = config['mass_pars']
        self.mass_names  = config['mass_names']


    def mass_ranges(self):
        quantities = self.analyzer.quantities(False)
        ranges = self.fit_ranges(quantities)
        return ranges

    def evaluate(self):
        ranges = self.mass_ranges()
        return self.analyzer.quantities(True, ranges)


    def fit_quantity(self, quant, func, par, names, pref):
        canvas = get_canvas(1./ 2., 1, True)
        adjust_canvas(canvas)
        ticks(canvas)

        fitquant = ROOT.TF1("fitquant" + pref, func)
        fitquant.SetLineColor(46)

        quant.Draw()
        fitquant.SetParameters(*par)
        fitquant.SetParNames(*names)

        # Doesn't fit and use default parameters for 
        # width/mass, therefore this will give correct estimation
        if not self.fit:
            [fitquant.FixParameter(i, p) for i, p in enumerate(par)]


        quant.Fit(fitquant, "q")

        # print [fitquant.GetParameter(i) for i, p in enumerate(par)]
        quant.SetLineColor(37)
        wait(pref + "-paramerisation-" + self.analyzer.label, self.analyzer.show_img, True)
        return fitquant

        
    def fit_ranges(self, quantities):
        ROOT.gStyle.SetOptStat('')
        mass, sigma = quantities.mass, quantities.width

        fitsigma = self.fit_quantity(sigma, self.width_func, self.width_pars, self.width_names, 'width')
        fitmass = self.fit_quantity(mass, self.mass_func, self.mass_pars, self.mass_names, 'mass')

        mass_range = lambda pt: (fitmass.Eval(pt) - self.nsigmas * fitsigma.Eval(pt),
                                 fitmass.Eval(pt) + self.nsigmas * fitsigma.Eval(pt))

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
