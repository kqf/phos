import unittest
import ROOT
from vault.datavault import DataVault
from tools.ep import EpRatioEstimator
from spectrum.options import EpRatioOptions
from spectrum.comparator import Comparator

from spectrum.processing import DataSlicer, InvariantMassExtractor
from spectrum.options import Options
from spectrum.pipeline import Pipeline
from spectrum.transformer import TransformerBase
from spectrum.output import AnalysisOutput


class ExtractMass(TransformerBase):

    def __init__(self, options=Options(), plot=False):
        super(ExtractMass, self).__init__(plot)
        self.options = options
        self.pipeline = Pipeline([
            ("slice", DataSlicer(options.analysis.pt)),
            ("parametrize", InvariantMassExtractor(options.analysis.invmass)),
        ])


class DebugEpRatio(unittest.TestCase):

    @unittest.skip("")
    def test_ep_ratio(self):
        options = EpRatioOptions()
        options.histname = "hEp_ele"
        estimator = ExtractMass(options, plot=True)
        output = estimator.transform(
            DataVault().input(
                "pythia8",
                version="ep_ratio_1",
                listname="PHOSEpRatioCoutput1",
                histname="Ep_ele",
                use_mixing=False),
            loggs=AnalysisOutput("test ep ratio estimator")
        )

        for o in output:
            func = ROOT.TF1('func', "gaus(0)", 0.8, 1.2)
            func.SetParameter(0, 1)
            func.SetParameter(1, 1)
            func.SetParameter(2, 1)
            o.mass.Fit(func, "R")
            Comparator().compare(o.mass)
            # Comparator().compare(o.mass)


class TestEpRatio(unittest.TestCase):

    # @unittest.skip("")
    def test_ep_ratio(self):
        options = EpRatioOptions()
        options.histname = "hEp_ele"
        estimator = EpRatioEstimator(options, plot=True)
        output = estimator.transform(
            DataVault().input(
                "pythia8",
                version="ep_ratio_1",
                listname="PHOSEpRatioCoutput1",
                histname="Ep_ele",
                use_mixing=False),
            "test ep ratio estimator"
        )
        for o in output:
            Comparator().compare(o)
