import unittest
import ROOT

from tools.feeddown import FeeddownEstimator
from vault.datavault import DataVault

from spectrum.options import FeeddownOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator


def feeddown_paramerization():
    func_feeddown = ROOT.TF1(
        "func_feeddown",
        "[2] * (1.+[0]*TMath::Exp(-x/2*x/2/2./[1]/[1]))",
        0, 100
    )
    func_feeddown.SetParNames("A", "#sigma", "E_{scale}")
    func_feeddown.SetParameter(0, -1.4)
    func_feeddown.SetParameter(1, 0.33)
    func_feeddown.SetParLimits(1, 0, 10)
    func_feeddown.SetParameter(2, 0.02)
    return func_feeddown


class FeddownTest(unittest.TestCase):
    def test_feeddown_correction(self):
        options = FeeddownOptions()
        options.fitf = feeddown_paramerization()
        estimator = FeeddownEstimator(options)
        loggs = AnalysisOutput("feeddown nlo correction")
        output = estimator.transform(
            [
                DataVault().input(
                    "pythia8",
                    listname="MCStudy",
                    use_mixing=False,
                    histname="MassPt_#pi^{0}_primary_#Lambda",
                ),
                DataVault().input("pythia8", listname="FeeddownSelection"),
            ],
            loggs
        )
        loggs.plot()
        Comparator().compare(output)
        self.assertGreater(output.GetEntries(), 0)
