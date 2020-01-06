import ROOT


def parametrisation(options):
    ptype = {
        "CrystalBall": CrystalBall,
        "Gaus": Gaus,
    }.get(options.fitf, None)
    return ptype(options)


class PeakParametrisation(object):
    pols = {
        "pol1": "[{start} + 0] + [{start} + 1]*x",
        "pol2": "[{start} + 0] + [{start} + 1]*(x-{mass:.3f}) + [{start} + 2]*(x-{mass:.3f})^2",  # noqa
        "pol3": "[{start} + 0] + [{start} + 1]*(x-{mass:.3f}) + [{start} + 2]*(x-{mass:.3f})^2 + [{start} + 3] * x^(x-{mass:.3f})^3",  # noqa
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
        # Initiate signal function
        signal = self.form_fitting_function(self.npars_signal)
        background = self.form_background()

        # Create the total fitting function
        fitfun = ROOT.TF1("fitfun", "({}) + ({})".format(signal, background))
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
        self.background = ROOT.TF1(
            "background",
            self.form_background(0), *self.opt.fit_range)
        self._set_background_parameters(fitfun, self.background)
        return fitfun, self.background

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
        template = self.pols[self.opt.background]
        return template.format(start=self.npars_signal, mass=self.opt.fit_mass)


class CrystalBall(PeakParametrisation):
    npars_signal = 5

    def __init__(self, options):
        super(CrystalBall, self).__init__(options)

    def form_fitting_function(self, name="signal"):
        # alpha, n = "[3]", "[4]" (alpha >= 0, n > 1)
        a = "TMath::Exp(-[3] * [3] / 2.) * TMath::Power([4] / [3], [4])"
        b = "[4] / [3] - [3]"
        gaus = "[0]*exp(-(x-[1])*(x-[1])/(2*[2]*[2]))"
        shoulder = "[0]*{a}*({b}-(x-[1])/[2])^(-[4])".format(a=a, b=b)
        cball = "((x-[1])/[2] > -[3] ? {gaus} : {shoulder})"
        return cball.format(gaus=gaus, shoulder=shoulder)

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
    npars_signal = 3

    def __init__(self, options):
        super(Gaus, self).__init__(options)

    def form_fitting_function(self, name="signal"):
        return "gaus(0)"

    def _setup_parameters(self, fitfun, pars):
        fitfun.SetParameters(*pars)
        fitfun.SetParameter(1, self.opt.fit_mass)
        # fitfun.SetParameter(2, self.opt.fit_width)

    def _setup_limits(self, fitfun, maximum):
        fitfun.SetParLimits(0, 0., maximum * 1.5)
        fitfun.SetParLimits(1, *self.opt.fit_mass_limits)
        fitfun.SetParLimits(2, *self.opt.fit_width_limits)
