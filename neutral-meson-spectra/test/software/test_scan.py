import unittest
from tools.scan import NonlinearityScan
from vault.datavault import DataVault
from spectrum.options import NonlinearityScanOptions
from spectrum.output import AnalysisOutput
from tqdm import trange


class TestScan(unittest.TestCase):

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
