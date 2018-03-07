#!/usr/bin/python

import ROOT

class PeakParametrisation(object):

    def __init__(self, options):
        super(PeakParametrisation, self).__init__()
        ROOT.gStyle.SetOptFit()

        self.opt = options
        funcname = self.__class__.__name__
        # Initiate signal function
        self.signal = self.form_fitting_function(funcname)

    def fit(self, hist):
        if (not hist) or (hist.GetEntries() == 0): 
            return None, None

        background = self.form_background()

        formula = "{0} + {1}".format(self.signal.GetName(), background.GetName())
        fitfun = ROOT.TF1("fitfun", formula, *self.opt.fit_range)

        self.setup_parameters(fitfun, hist)

        if 'mix' in hist.GetName().lower():
            fitfun.FixParameter(0, 0)

        fitfun.SetNpx(1000)
        hist.Fit(fitfun,"RQ", "")

        npar, nparb = fitfun.GetNpar(), background.GetNpar()
        for i in range(0, nparb):
            parameter = fitfun.GetParameter(npar - (nparb - i))
            background.SetParameter(i, parameter)
        return fitfun, background


    def preliminary_fit(self, hist):
        # make a preliminary fit to estimate parameters
        ff = ROOT.TF1("fastfit", "gaus(0) + [3]")
        ff.SetParLimits(0, 0., hist.GetMaximum() * 1.5)
        ff.SetParLimits(1, *self.opt.prel_mass_limits)
        ff.SetParLimits(2, *self.opt.prel_width_limits)
        ff.SetParameters(hist.GetMaximum()/3., *self.opt.prel_paremeters)
        hist.Fit(ff, "0QL", "", *self.opt.prel_range)
        return [ff.GetParameter(i) if i != 1 else self.opt.fit_mass for i in range(4)]


    def setup_parameters(self, fitfun, hist):
        fitfun.SetParNames(*self.opt.par_names)
        fitfun.SetLineColor(46)
        fitfun.SetLineWidth(2)
        fitfun.SetParLimits(0, 0., hist.GetMaximum() * 1.5)
        fitfun.SetParLimits(1, *self.opt.fit_mass_limits)
        fitfun.SetParLimits(2, *self.opt.fit_width_limits)
        pars = self.preliminary_fit(hist) 
        fitfun.SetParameters(*pars)
        return pars

    def form_background(self, fname = "background"):
        if 'pol2' in self.opt.background:
            bf = "[0] + [1]*(x-%.3f) + [2]*(x-%.3f)^2"
            return ROOT.TF1(fname, bf % tuple([self.opt.fit_mass] * 2), *self.opt.fit_range)

        if 'pol3' in self.opt.background:
            bf = "[0] + [1]*(x-%.3f) + [2]*(x-%.3f)^2 + [3] * x^(x-%.3f)^3"
            return ROOT.TF1(fname, bf % tuple([self.opt.fit_mass] * 3) , *self.opt.fit_range)


        return ROOT.TF1(fname, self.opt.background + "(0)", *self.opt.fit_range)


    @staticmethod
    def get(options):
        par = {'CrystalBall': CrystalBall, 'Gaus': Gaus}.get(options.fitf, None)
        if not par:
            raise AttributeError('There is no such parametrization as {}'.format(options.fitf))
        obj = par(options)
        return obj
        

class CrystalBall(PeakParametrisation):

    def __init__(self, options):
        super(CrystalBall, self).__init__(options)


    def form_fitting_function(self, name = 'cball'):
        alpha, n = '[3]', '[4]' # alpha >= 0, n > 1
        a = 'TMath::Exp(-[3] * [3] / 2.) * TMath::Power([4] / [3], [4])'
        b = '[4] / [3] - [3]'
        cff = "(x-[1])/[2] > -%s ? [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2])) : [0]*%s*(%s-(x-[1])/[2])^(-%s)"
        signal = ROOT.TF1(name, cff % (alpha, a, b, n))
        return signal


    def setup_parameters(self, fitfun, hist):
        pars = super(CrystalBall, self).setup_parameters(fitfun, hist)
        fitfun.SetParLimits(3, *self.opt.cb_alpha_limits)
        fitfun.SetParLimits(4, *self.opt.cb_n_limits)
        fitfun.SetParameters(*(pars[:3] + [self.opt.cb_alpha, self.opt.cb_n] + pars[3:]))

        if not self.opt.relaxed:
            fitfun.FixParameter(3, self.opt.cb_alpha)
            fitfun.FixParameter(4, self.opt.cb_n) 



class Gaus(PeakParametrisation):
    def __init__(self, options):
        super(Gaus, self).__init__(options)


    def form_fitting_function(self, name = 'cball'):
        signal = ROOT.TF1(name, "gaus(0)")
        return signal

