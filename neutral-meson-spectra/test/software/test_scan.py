import unittest
from tools.scan import NonlinearityScan
from vault.datavault import DataVault
from spectrum.options import NonlinearityScanOptions
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.output import AnalysisOutput
from collections import OrderedDict
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

    # @unittest.skip('')
    def test_composite_interface(self):
        prod = "single #pi^{0} nonlinearity scan"
        nbins = 4
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

        unified_inputs = OrderedDict([
            (low, (0.0, 8.0)),
            (high, (4.0, 20.0)),
        ])

        estimator = NonlinearityScan(
            CompositeNonlinearityScanOptions(unified_inputs, nbins=nbins)
        )

        low, high = low.read_multiple(2), high.read_multiple(2)
        mc_data = [(l, h) for l, h in zip(low, high)]

        print estimator.transform(
            [DataVault().input("data")] + mc_data,
            loggs=AnalysisOutput("testing the scan interface")
        )
        # loggs.plot()