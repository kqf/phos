import pytest

import ROOT
from spectrum.analysis import Analysis
from spectrum.comparator import Comparator
from spectrum.options import Options
from spectrum.output import open_loggs
from spectrum.pipeline import Pipeline
from spectrum.pipeline import TransformerBase
from vault.datavault import DataVault


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0")


class CbFitOptions(object):
    def __init__(self, particle):
        super(CbFitOptions, self).__init__()
        self.analysis = Options(particle)
        self.analysis.invmass.signal.relaxed = True
        self.analysis.invmass.background.relaxed = True

        self.names = ["cball_alpha", "cball_n"]
        self.functions = [
            ROOT.TF1("alpha", "pol0", 0, 20),
            ROOT.TF1("n", "pol0", 0, 20),
        ]


class SelectAndFitHistograms(TransformerBase):

    def __init__(self, options=None):
        self.options = options

    def transform(self, data, loggs):
        output = [data._asdict()[n] for n in self.options.names]
        for hist, func in zip(output, self.options.functions):
            self._fit_histogram(hist, func)
        return output

    def _fit_histogram(self, histogram, func):
        histogram.Fit(func, 'q')
        histogram.SetLineColor(ROOT.kBlue + 1)
        func.SetLineColor(ROOT.kRed + 1)
        val, err = func.GetParameter(0), func.GetParError(0)
        print("The scale is", histogram.GetTitle(), val, err)


class CballParametersEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(CballParametersEstimator, self).__init__(plot)
        self.pipeline = Pipeline([
            ('analysis', Analysis(options.analysis, plot)),
            ('cball', SelectAndFitHistograms(options)),
        ])


@pytest.mark.interactive
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta"
])
def test_cball_parameters(particle, data):
    estimator = CballParametersEstimator(
        CbFitOptions(particle=particle), plot=False)

    with open_loggs("test cball parameters {}".format(particle)) as loggs:
        hists = estimator.transform(data, loggs=loggs)

    for h in hists:
        Comparator().compare(h)
