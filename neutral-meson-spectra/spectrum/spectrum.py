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
        self.width_pars  = self.conf['width_pars']
        self.width_names = self.conf['width_names']
        self.mass_pars   = self.conf['mass_pars']
        self.mass_names  = self.conf['mass_names']


    def mass_ranges(self):
        quantities = self.analyzer.quantities()
        ranges = self.fit_ranges(quantities)
        return ranges

    def evaluate(self):
        ranges = self.mass_ranges()
        return self.analyzer.quantities(ranges)

    def fit_ranges(self, quantities):
        ROOT.gStyle.SetOptStat('')
        # TODO: split this method in two smaller ones
        mass, sigma = quantities[0:2]
        canvas = get_canvas(1./ 2., 1, True)

        canvas.Divide(1, 1, *self.canvas)
        pad = canvas.cd()
        pad.SetTickx()
        pad.SetTicky() 
        pad.SetGridx()
        pad.SetGridy()

        fitsigma = ROOT.TF1("fitsigma", "TMath::Exp([0] + [1] * x ) * [2] * x + [3]", 
            0.999* sigma.GetBinCenter(0), sigma.GetBinCenter(sigma.GetNbinsX()))

        sigma.Draw()
        fitsigma.SetParameters(*self.width_pars)
        fitsigma.SetParNames(*self.width_names)

        sigma.Fit(fitsigma, "rq")
        sigma.SetLineColor(38)
        wait("width-paramerisation-" + self.analyzer.label, self.analyzer.show_img)

        pad = canvas.cd()
        pad.SetTickx()
        pad.SetTicky() 
        pad.SetGridx()
        pad.SetGridy()
        mass.Draw()
        fitmass = ROOT.TF1("fitmass", "TMath::Exp([0] + [1] * x ) * [2] * x + [3]", 
            0.999* mass.GetBinCenter(0), mass.GetBinCenter(mass.GetNbinsX()))

        fitmass.SetParameters(*self.mass_pars)
        fitmass.SetParNames(*self.mass_names)
        fitmass.SetLineColor(46)
        mass.Fit(fitmass, "rq")
        mass.SetLineColor(38)


        if canvas: canvas.Update()
        mass_range = lambda pt: (fitmass.Eval(pt) - self.nsigmas * fitsigma.Eval(pt),
                                 fitmass.Eval(pt) + self.nsigmas * fitsigma.Eval(pt))


        wait("mass-paramerisation-" + self.analyzer.label, self.analyzer.show_img)

        pt_values = [mass.GetBinCenter(i + 1) for i in range(mass.GetNbinsX())]
        return map(mass_range, pt_values) 
