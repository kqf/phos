#!/usr/bin/python

import ROOT
import json

class PeakParametrisation(object):
    with open('config/peak-parameters.json') as f:
        configuration = json.load(f)

    def __init__(self, ispi0peak):
        super(PeakParametrisation, self).__init__()
        ROOT.gStyle.SetOptFit()
        self.ispi0peak = ispi0peak

        name = 'pi0' if self.ispi0peak else 'eta'
        self.d = self.configuration[name]

        self.fit_range         = self.d["fit_range"]
        self.prel_mass_limits  = self.d["prel_mass_limits"]
        self.prel_width_limits = self.d["prel_width_limits"]
        self.prel_range        = self.d["prel_range"]
        self.prel_paremeters   = self.d["prel_paremeters"]
        self.fit_mass          = self.d["fit_mass"]
        self.fit_mass_limits   = self.d["fit_mass_limits"]
        self.fit_width_limits  = self.d["fit_width_limits"]


    def fit(self):
        return None, None


    def preliminary_fit(self, hist):
        # make a preliminary fit to estimate parameters
        ff = ROOT.TF1("fastfit", "gaus(0) + [3]")
        ff.SetParLimits(0, 0., hist.GetMaximum() * 1.5)
        ff.SetParLimits(1, *self.prel_mass_limits)
        ff.SetParLimits(2, *self.prel_width_limits)
        ff.SetParameters(hist.GetMaximum()/3., *self.prel_paremeters)
        hist.Fit(ff, "0QL", "", *self.prel_range)
        return [ff.GetParameter(i) for i in range(4)]
        

class CrystalBall(PeakParametrisation):
    def __init__(self, fit_range, relaxed):
        super(CrystalBall, self).__init__(fit_range)
        self.relaxed = relaxed

        self.cb_n = self.d["cb_n"]
        self.cb_alpha = self.d["cb_alpha"]
        self.cb_n_limits = self.d["cb_n_limits"]
        self.cb_alpha_limits = self.d["cb_alpha_limits"]
        

    def form_fitting_function(self, name = 'cball'):
        alpha, n = '[3]', '[4]' # alpha >= 0, n > 1
        a = 'TMath::Exp(-[3] * [3] / 2.) * TMath::Power([4] / [3], [4])'
        b = '[4] / [3] - [3]'
        signal = ROOT.TF1("cball", "(x-[1])/[2] > -%s ? [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2])) : [0]*%s*(%s-(x-[1])/[2])^(-%s)" % (alpha, a, b, n) )
        return signal


    def setup_parameters(self, fitfun, hist):
        fitfun.SetParNames("A", "M", "#sigma", "#alpha", "n", "a_{0}", "a_{1}", "a_{2}")
        fitfun.SetLineColor(46)
        fitfun.SetLineWidth(2)
        fitfun.SetParLimits(0, 0., hist.GetMaximum() * 1.5)
        fitfun.SetParLimits(1, *self.fit_mass_limits)
        fitfun.SetParLimits(2, *self.fit_width_limits)
        fitfun.SetParLimits(3, *self.cb_alpha_limits)
        fitfun.SetParLimits(4, *self.cb_n_limits)
        pars = self.preliminary_fit(hist) 
        fitfun.SetParameters(*(pars[:3] + [self.cb_alpha, self.cb_n] + pars[3:]))

        if not self.relaxed:
            fitfun.FixParameter(3, self.cb_alpha)
            fitfun.FixParameter(4, self.cb_n) 

    def fit(self, hist, skipbgrnd = False):
        if (not hist) or (hist.GetEntries() == 0): return None, None

        # Initiate signal function
        signal = self.form_fitting_function('cball')

        # background
        background = ROOT.TF1("mypol2", "[0] + [1]*(x-%.3f) + [2]*(x-%.3f)^2" % (self.fit_mass, self.fit_mass), *self.fit_range)

        # signal + background
        fitfun = ROOT.TF1("fitfun", "cball + mypol2", *self.fit_range)
        self.setup_parameters(fitfun, hist)

        # For background extraction
        npar = fitfun.GetNpar()

        # Fit witout background
        if skipbgrnd:
            fitfun.FixParameter(npar - 3, 0)
            fitfun.FixParameter(npar - 2, 0)
            fitfun.FixParameter(npar - 1, 0)

        if 'mix' in hist.GetName().lower():
            fitfun.FixParameter(0, 0)

        hist.Fit(fitfun,"QR", "")

        background.SetParameter(0, fitfun.GetParameter(npar - 3))
        background.SetParameter(1, fitfun.GetParameter(npar - 2))
        background.SetParameter(2, fitfun.GetParameter(npar - 1))
        return fitfun, background
