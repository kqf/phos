import unittest
import ROOT

from spectrum.spectrum import Spectrum
from spectrum.input import Input
from spectrum.sutils import ticks
from spectrum.options import Options


from spectrum.analysis import Analysis
from spectrum.transformer import TransformerBase
from spectrum.pipeline import Pipeline
from vault.datavault import DataVault
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator


class CbFitOptions(object):
    def __init__(self, particle):
        super(CbFitOptions, self).__init__()
        self.analysis = Options(particle, relaxedcb=True)
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
        histogram.SetLineColor(37)
        func.SetLineColor(46)
        print "The scale is", histogram.GetTitle(), func.GetParameter(0)


class CballParametersEstimator(TransformerBase):
    def __init__(self, options, plot=False):
        super(CballParametersEstimator, self).__init__(plot)
        self.pipeline = Pipeline([
            ('analysis', Analysis(options.analysis, plot)),
            ('cball', SelectAndFitHistograms(options)),
        ])


class CrystalBallParametersPi0(unittest.TestCase):

    def setUp(self):
        self.particle = "#pi^{0}"

    def test_parameters(self):
        options = CbFitOptions(particle=self.particle)
        estimator = CballParametersEstimator(options, plot=False)
        hists = estimator.transform(
            DataVault().input("data"),
            loggs=AnalysisOutput(
                "test cball parameters for %s" % self.particle
            ),
        )
        for h in hists:
            Comparator().compare(h)


class CrystalBallParametersEta(CrystalBallParametersPi0):

    def setUp(self):
        self.particle = "#eta"
