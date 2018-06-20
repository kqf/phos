import unittest
from tools.scan import NonlinearityScan
from vault.datavault import DataVault
from spectrum.options import NonlinearityScanOptions
from spectrum.output import AnalysisOutput
from tqdm import trange


class TestScan(unittest.TestCase):

    @unittest.skip('')
    def test_interface(self):
        nbins = 2
        estimator = NonlinearityScan(
            NonlinearityScanOptions(nbins=nbins)
        )

        mc = [
            DataVault().input(
                "pythia8",
                "staging",
                listname="PhysNonlinScan",
                histname="MassPt_{}_{}".format(i, j)
            )
            for j in trange(nbins) for i in trange(nbins)
        ]

        print estimator.transform(
            [DataVault().input("data")] + mc,
            loggs=AnalysisOutput("testing the scan interface")
        )

    def test_composite_interface(self):
        production = "single #pi^{0} nonlin scan"
        nbins = 2
        estimator = NonlinearityScan(
            NonlinearityScanOptions(nbins=nbins)
        )

        unified_inputs = {
            DataVault().input(production, "low", "PhysEff"): (0.0, 8.0),
            DataVault().input(production, "high", "PhysEff"): (4.0, 20.0),
        }

        print estimator.transform(
            [DataVault().input("data")] + unified_inputs.values(),
            loggs=AnalysisOutput("testing the scan interface")
        )
