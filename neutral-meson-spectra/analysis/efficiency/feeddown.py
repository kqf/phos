import unittest
import ROOT

from tools.feeddown import FeeddownEstimator
from vault.datavault import DataVault

from spectrum.options import FeeddownOptions
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
    func_feeddown.FixParameter(2, 0.02)
    return func_feeddown


class FeddownTest(unittest.TestCase):
    def test_feeddown_correction(self):
        options = FeeddownOptions()
        options.fitf = feeddown_paramerization()
        estimator = FeeddownEstimator(
            options
        )

        output, errors = estimator.transform(
            [
                DataVault().input(
                    "pythia8",
                    "staging",
                    listname="MCStudy",
                    use_mixing=False,
                    histname="MassPt_#pi^{0}_feeddown_K^{s}_{0}"
                ),
                DataVault().input("pythia8", "stable",
                                  listname="MCStudyOnlyTender"),
            ],
            "test the feeddown correction"
        )
        title = "Feeddown correction approximation"
        title += "; p_{T}, GeV/c"
        title += "; #frac{dN(#pi^{0} #leftarrow K_{0}^{s})}{dp_{T}} / "
        title += "#frac{dN(all)}{dp_{T}}"
        output.SetTitle(title)
        errors.SetTitle(title)
        errors.label = "approximation"
        errors.SetOption("e3")
        output.logy = False
        errors.SetFillStyle(3002)
        output.Scale(1. / 1.5)
        Comparator(rrange=(-1, -1)).compare(output, errors)
