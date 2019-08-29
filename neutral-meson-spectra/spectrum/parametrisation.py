import ROOT

from spectrum.broot import BROOT as br


def parametrisation(options):
    ptype = {
        'CrystalBall': CrystalBall,
        'Gaus': Gaus,
    }.get(options.fitf, None)
    return ptype(options)


class PeakParametrisation(object):
    pols = {
        "pol1": "[0] + [1]*x",
        "pol2": "[0] + [1]*(x-{mass:.3f}) + [2]*(x-{mass:.3f})^2",
        "pol3": "[0] + [1]*(x-{mass:.3f}) + [2]*(x-{mass:.3f})^2 + [3] * x^(x-{mass:.3f})^3",  # noqa
    }

    def __init__(self, options):
        super(PeakParametrisation, self).__init__()
        ROOT.gStyle.SetOptFit()
        self.opt = options

    def _set_background_parameters(self, fitfun, background):
        npar, nparb = fitfun.GetNpar(), background.GetNpar()
        for i in range(0, nparb):
            parameter = fitfun.GetParameter(npar - (nparb - i))
            background.SetParameter(i, parameter)

    def _set_no_signal(self, fitfun, is_mixing=False):
        if not is_mixing:
            return
        fitfun.FixParameter(0, 0)

    def fit(self, hist, is_mixing=False):
        if (not hist) or (hist.GetEntries() == 0):
            return None, None

        # Initiate signal function
        signal = self.form_fitting_function()
        background = self.form_background()
        fitfun = br.tf1_sum(signal, background)
        fitfun.SetRange(*self.opt.fit_range)
        fitfun.SetNpx(1000)
        fitfun.SetParNames(*self.opt.par_names)
        fitfun.SetLineColor(46)
        fitfun.SetLineWidth(2)
        pars = self._preliminary_fit(hist)

        self._setup_limits(fitfun, hist.GetMaximum())
        self._setup_parameters(fitfun, pars)
        self._set_no_signal(fitfun, is_mixing)
        hist.Fit(fitfun, "RQM", "")
        self._set_background_parameters(fitfun, background)
        return fitfun, background

    def _preliminary_fit(self, hist):
        # make a preliminary fit to estimate parameters
        ff = ROOT.TF1("fastfit", "gaus(0) + [3]")
        ff.SetParLimits(0, 0., hist.GetMaximum() * 1.5)
        ff.SetParLimits(1, *self.opt.preliminary.mass_limits)
        ff.SetParLimits(2, *self.opt.preliminary.width_limits)
        ff.SetParameters(*self.opt.preliminary.parameters)
        ff.SetParameter(0, hist.GetMaximum() / 3.)
        hist.Fit(ff, "0QL", "", *self.opt.preliminary.range)
        par = [ff.GetParameter(i) for i in range(4)]
        par[1] = self.opt.fit_mass
        return par

    def form_background(self, fname="background"):
        pol = self.pols[self.opt.background].format(mass=self.opt.fit_mass)
        return ROOT.TF1(fname, pol, *self.opt.fit_range)


class CrystalBall(PeakParametrisation):

    def __init__(self, options):
        super(CrystalBall, self).__init__(options)

    def form_fitting_function(self, name='signal'):
        # alpha, n = '[3]', '[4]' (alpha >= 0, n > 1)
        a = 'TMath::Exp(-[3] * [3] / 2.) * TMath::Power([4] / [3], [4])'
        b = '[4] / [3] - [3]'
        cff = "(x-[1])/[2] > -[3] ? [0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2])) : " \
            "[0]*{a}*({b}-(x-[1])/[2])^(-[4])"
        signal = ROOT.TF1(name, cff.format(a=a, b=b))
        return signal

    def _setup_parameters(self, fitfun, pars):
        fitfun.SetParameters(
            *(pars[:3] + [self.opt.cb_alpha, self.opt.cb_n] + pars[3:]))

        if not self.opt.relaxed:
            fitfun.FixParameter(3, self.opt.cb_alpha)
            fitfun.FixParameter(4, self.opt.cb_n)

    def _setup_limits(self, fitfun, maximum):
        fitfun.SetParLimits(0, 0., maximum * 1.5)
        fitfun.SetParLimits(1, *self.opt.fit_mass_limits)
        fitfun.SetParLimits(2, *self.opt.fit_width_limits)
        fitfun.SetParLimits(3, *self.opt.cb_alpha_limits)
        fitfun.SetParLimits(4, *self.opt.cb_n_limits)


class Gaus(PeakParametrisation):
    def __init__(self, options):
        super(Gaus, self).__init__(options)

    def form_fitting_function(self, name='signal'):
        signal = ROOT.TF1(name, "gaus")
        return signal

    def _setup_parameters(self, fitfun, pars):
        fitfun.SetParameters(*pars)

    def _setup_limits(self, fitfun, maximum):
        fitfun.SetParLimits(0, 0., maximum * 1.5)
        fitfun.SetParLimits(1, *self.opt.fit_mass_limits)
        fitfun.SetParLimits(2, *self.opt.fit_width_limits)
