#!/usr/bin/python

import ROOT
import json
from sutils import get_canvas, wait
from ptanalyzer import PtAnalyzer
from options import Options


ROOT.TH1.AddDirectory(False)


class Spectrum(object):
    with open('config/spectrum.json') as f:
        conf = json.load(f)

    def __init__(self, lst, label ='N_{cell} > 3', mode = 'v', nsigmas = 2, options = Options()):
        super(Spectrum, self).__init__()
        self.nsigmas = nsigmas
        self.analyzer = PtAnalyzer(lst, label, mode, options)
        
        self.canvas      = self.conf['canvas']
        self.width_func  = self.conf['width_func']
        self.width_pars  = self.conf['width_pars']
        self.width_names = self.conf['width_names']

        self.mass_func   = self.conf['mass_func']
        self.mass_pars   = self.conf['mass_pars']
        self.mass_names  = self.conf['mass_names']


    def mass_ranges(self):
        quantities = self.analyzer.quantities()
        ranges = self.fit_ranges(quantities)
        return ranges

    def evaluate(self):
        ranges = self.mass_ranges()
        return self.analyzer.quantities(ranges)


    def fit_quantity(self, quant, func, par, names, pref):
        canvas = get_canvas(1./ 2., 1, True)

        canvas.Divide(1, 1, *self.canvas)
        pad = canvas.cd()
        pad.SetTickx()
        pad.SetTicky() 
        pad.SetGridx()
        pad.SetGridy()

        fitquant = ROOT.TF1("fitquant" + pref, func, quant.GetBinCenter(1), quant.GetBinCenter(quant.GetNbinsX()))

        quant.Draw()
        fitquant.SetParameters(*par)
        fitquant.SetParNames(*names)

        quant.Fit(fitquant, "rq")
        quant.SetLineColor(38)
        wait(pref + "-paramerisation-" + self.analyzer.label, self.analyzer.show_img)
        return fitquant

        
    def fit_ranges(self, quantities):
        ROOT.gStyle.SetOptStat('')
        mass, sigma = quantities[0:2]

        fitsigma = self.fit_quantity(sigma, self.width_func, self.width_pars, self.width_names, 'width')
        fitmass = self.fit_quantity(mass, self.mass_func, self.mass_pars, self.mass_names, 'mass')

        mass_range = lambda pt: (fitmass.Eval(pt) - self.nsigmas * fitsigma.Eval(pt),
                                 fitmass.Eval(pt) + self.nsigmas * fitsigma.Eval(pt))

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
