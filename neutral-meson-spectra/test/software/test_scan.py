import unittest

from spectrum.options import (CompositeNonlinearityScanOptions,
                              NonlinearityScanOptions)
from spectrum.output import AnalysisOutput
from tools.scan import NonlinearityScan
from tqdm import trange
from vault.datavault import DataVault


class TestScan(unittest.TestCase):

    def test_interface(self):
        nbins = 2
        estimator = NonlinearityScan(
            NonlinearityScanOptions(nbins=nbins)
        )

        mc = [
            DataVault().input(
                "pythia8",
                listname="PhysNonlinScan",
                histname="MassPt_{}_{}".format(i, j)
            )
            for j in trange(nbins) for i in trange(nbins)
        ]

        assert estimator.transform(
            (DataVault().input("data"), mc),
            loggs=AnalysisOutput("testing the scan interface")
        )

    def test_composite_interface(self):
        prod = "single #pi^{0} nonlinearity scan"
        nbins = 2
        histnames = sum([
            [
                "hMassPt_{}_{}".format(i, j),
                "hMixMassPt_{}_{}".format(i, j),
            ]
            for j in range(nbins)
            for i in range(nbins)
        ], [])

        low = DataVault().input(prod, "low", inputs=histnames)
        high = DataVault().input(prod, "high", inputs=histnames)

        estimator = NonlinearityScan(
            CompositeNonlinearityScanOptions(nbins=nbins)
        )

        low, high = low.read_multiple(2), high.read_multiple(2)
        mc_data = [(l, h) for l, h in zip(low, high)]

        assert estimator.transform(
            (DataVault().input("data"), mc_data),
            loggs=AnalysisOutput("testing the scan interface")
        )
