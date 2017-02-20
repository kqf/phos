#!/usr/bin/python

import ROOT

class PeakParametrization(object):
    def __init__(self, ispi0peak):
        super(PeakParametrization, self).__init__()
        ROOT.gStyle.SetOptFit()
        self.ispi0peak = ispi0peak

        # All "magic" numbers should be here 
        # Constrains on pi0/eta spectrum
        #
        # TODO: Should I move these parameters to json/pickle file?

        self.fit_range =         (0.05, 0.3)        if ispi0peak else (0.4, 6.8)

        self.prel_mass_limits =  (0.1, 0.2)         if ispi0peak else (0.5, 0.6)
        self.prel_width_limits = (0.004, 0.030)     if ispi0peak else (0.004, 0.030)
        self.prel_range =        (0.105, 0.165)     if ispi0peak else (0.49, 0.6)
        self.prel_paremeters =   (0.135, 0.010, 0.) if ispi0peak else (0.547, 0.010, 0.)

        self.fit_mass = 0.135 if ispi0peak else 0.547
        self.fit_mass_limits =   (0.12, 0.15)       if ispi0peak else (0.520, 0.570)
        self.fit_width_limits =  (0.004, 0.030)     if ispi0peak else (0.004,0.050) 


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
        

class CrystalBall(PeakParametrization):
    """docstring for CrystalBall"""
    def __init__(self, fit_range, relaxed):
        super(CrystalBall, self).__init__(fit_range)
        self.relaxed = relaxed
        

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
        fitfun.SetParLimits(0, 0., hist.GetMaximum()*1.5)
        fitfun.SetParLimits(1, *self.fit_mass_limits)
        fitfun.SetParLimits(2, *self.fit_width_limits)
        fitfun.SetParLimits(3, 0, 2)
        fitfun.SetParLimits(4, 1., 3.5)
        pars = self.preliminary_fit(hist) 
        fitfun.SetParameters(*(pars[:3] + [1.1, 2] + pars[3:]))

        if not self.relaxed:
            fitfun.FixParameter(3, 1.1)
            fitfun.FixParameter(4, 2) 

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

        hist.Fit(fitfun,"QLR", "")

        background.SetParameter(0, fitfun.GetParameter(npar - 3))
        background.SetParameter(1, fitfun.GetParameter(npar - 2))
        background.SetParameter(2, fitfun.GetParameter(npar - 1))

        return fitfun, background