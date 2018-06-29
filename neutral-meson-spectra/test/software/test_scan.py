import unittest
from tools.scan import NonlinearityScan
from vault.datavault import DataVault
from spectrum.options import CompositeOptions, Options
from spectrum.options import NonlinearityScanOptions
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
from collections import OrderedDict
from tqdm import trange
from spectrum.analysis import Analysis


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

    @unittest.skip('')
    def test_composite_interface(self):
        prod = "single #pi^{0} nonlin scan old"
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


class TestAnalysis(unittest.TestCase):
    @unittest.skip('')
    def test_composite(self):
        prod = "single #pi^{0} nonlin scan"
        unified_inputs = {
            DataVault().input(prod, "low", histname="MassPt_0_0"): (0.0, 8.0),
            DataVault().input(prod, "high", histname="MassPt_0_0"): (4.0, 20.0)
        }

        analysis = Analysis(
            CompositeOptions(unified_inputs, "#pi^{0}")
        )

        output = analysis.transform(
            unified_inputs,
            loggs=AnalysisOutput("test the composite analysis")
        )

        for o in output:
            Comparator().compare(o)

    def test_simple(self):
        analysis = Analysis(Options().spmc((4.0, 20), "#pi^{0}"), plot=True)

        prod = "single #pi^{0} nonlin scan"
        loggs = AnalysisOutput("test the single analysis")
        output = analysis.transform(
            DataVault().input(prod, "high", histname="MassPt_0_0"),
            loggs
        )
        loggs.plot()

        for o in output:
            Comparator().compare(o)
