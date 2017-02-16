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
    def __init__(self, fit_range):
        super(CrystalBall, self).__init__(fit_range)
        
    def cb_parameters(self):
        # crystal ball parameters (fixed by hand for EMCAL) TODO: PHOS parameters?
        alpha = 1.1  # alpha >= 0
        n = 2.       # n > 1

        # CB tail parameters
        a = ROOT.TMath.Exp(-alpha * alpha / 2.) * (n / alpha) ** n 
        b = n / alpha - alpha
        return alpha, n, a, b


    def form_fitting_function(self, name = 'cball'):
        # signal (crystal ball)
        alpha, n, a, b = self.cb_parameters()
        signal = ROOT.TF1("cball", "(x-[1])/[2] > -%f ? [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2])) : [0]*%f*(%f-(x-[1])/[2])^(-%f)" % (alpha, a, b, n) )
        return signal

 
    def fit(self, hist):
        if (not hist) or (hist.GetEntries() == 0): return None, None

        # Initiate signal function
        signal = self.form_fitting_function('cball')

        # background
        background = ROOT.TF1("mypol2", "[0] + [1]*(x-%.3f) + [2]*(x-%.3f)^2" % (self.fit_mass, self.fit_mass), *self.fit_range)

        # signal + background
        fitfun = ROOT.TF1("fitfun", "cball + mypol2", *self.fit_range)
        fitfun.SetParNames("A", "M", "#sigma", "a_{0}", "a_{1}", "a_{2}")
        fitfun.SetLineColor(46)
        fitfun.SetLineWidth(2)
        fitfun.SetParLimits(0, 0., hist.GetMaximum()*1.5)
        fitfun.SetParLimits(1, *self.fit_mass_limits)
        fitfun.SetParLimits(2, *self.fit_width_limits)
        fitfun.SetParameters(*self.preliminary_fit(hist))
        hist.Fit(fitfun,"QLR", "")

        # For background extraction
        background.SetParameter(0, fitfun.GetParameter(3))
        background.SetParameter(1, fitfun.GetParameter(4))
        background.SetParameter(2, fitfun.GetParameter(5))

        return fitfun, background

class FlexibleCrystalBall(object):
       def __init__(self, fit_range):
        super(CrystalBall, self).__init__(fit_range)
   

        def form_fitting_function(self, name = 'cball'):
            alpha = '[6]'   # alpha >= 0
            n = '[7]'       # n > 1
            a = 'ROOT.TMath.Exp(-[6] * [6] / 2.) * ([7] / [6]) ** [7]'
            b = '[7] / [6] - [6]'
            signal = ROOT.TF1("cball", "(x-[1])/[2] > -%s ? [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2])) : [0]*%s*(%s-(x-[1])/[2])^(-%s)" % (alpha, a, b, n) )
            return signal
    

if __name__ == '__main__':
    main()