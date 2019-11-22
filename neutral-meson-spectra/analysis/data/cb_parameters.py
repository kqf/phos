import pytest

import ROOT
import spectrum.broot as br
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.output import open_loggs
from spectrum.pipeline import Pipeline
from spectrum.pipeline import TransformerBase
from spectrum.plotter import plot


class CbFitOptions(object):
    def __init__(self, particle):
        super(CbFitOptions, self).__init__()
        self.analysis = Options(particle, pt="config/pt-same.json")
        self.analysis.invmass.signal.relaxed = True
        self.analysis.invmass.background.relaxed = True

        self.names = ["cball_alpha", "cball_n"]
        self.functions = [
            ROOT.TF1("alpha", "pol0", 0, 20),
            ROOT.TF1("n", "pol0", 0, 20),
        ]
        self.limits = (0., 4.), (0., 6.)


class SelectAndFitHistograms(TransformerBase):

    def __init__(self, options=None):
        self.opt = options

    def transform(self, data, loggs):
        output = [data._asdict()[n] for n in self.opt.names]
        args = zip(output, self.opt.functions, self.opt.limits)
        for hist, func, limits in args:
            self._fit_histogram(hist, func, self.opt.analysis.particle)
            hist.ylimits = limits
            hist.SetTitle("Data")
        return data._asdict()

    def _fit_histogram(self, histogram, func, particle):
        histogram.Fit(func, 'q')
        histogram.SetLineColor(ROOT.kRed + 1)
        func.SetLineColor(ROOT.kBlue + 1)
        func.SetLineWidth(2)
        func.SetParName(0, "Value")
        print()
        br.report(func, particle)


class CballParametersEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(CballParametersEstimator, self).__init__(plot)
        self.pipeline = Pipeline([
            ('analysis', Analysis(options.analysis, plot)),
            ('cball', SelectAndFitHistograms(options)),
        ])


@pytest.fixture
def hists(particle, data):
    estimator = CballParametersEstimator(
        CbFitOptions(particle=particle), plot=False)

    with open_loggs() as loggs:
        data = estimator.transform(data, loggs=loggs)
    return data


@pytest.fixture
def oname(particle, quantity):
    quantity = quantity.replace("cball_", "")
    pattern = "results/analysis/data/{}_{}.pdf"
    return pattern.format(quantity, br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
@pytest.mark.parametrize("quantity", [
    "cball_n",
    "cball_alpha",
])
def test_cball_parameters(particle, data, hists, quantity, oname, ltitle):
    hist = hists[quantity]
    func = hist.GetListOfFunctions()[0]
    func.SetTitle("Constant fit")
    func.SetLineStyle(9)
    func.SetLineColor(ROOT.kBlack)
    plot(
        [hist, func],
        logy=False,
        ylimits=hist.ylimits,
        legend_pos=(0.58, 0.7, 0.68, 0.85),
        ltitle=ltitle,
        oname=oname,
    )
