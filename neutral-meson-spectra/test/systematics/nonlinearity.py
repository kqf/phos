import unittest
from collections import OrderedDict

from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityScanOptions
from spectrum.output import AnalysisOutput
from tools.scan import NonlinearityScan, form_histnames
from vault.datavault import DataVault


class TestNonliearityUncertainty(unittest.TestCase):

    def test(self):
        prod = "single #pi^{0} scan nonlinearity6"
        histnames = form_histnames(self.nbins)
        low = DataVault().input(prod, "low", inputs=histnames)
        high = DataVault().input(prod, "high", inputs=histnames)

        unified_inputs = OrderedDict([
            (low, (0.0, 8.0)),
            (high, (4.0, 20.0)),
        ])
        options = CompositeNonlinearityScanOptions(
            unified_inputs, nbins=self.nbins)
        options.factor = 1.

        low, high = low.read_multiple(2), high.read_multiple(2)
        spmc = [(l, h) for l, h in zip(low, high)]

        chi2ndf = NonlinearityScan(options).transform(
            spmc,
            loggs=AnalysisOutput("testing the scan interface")
        )
        Comparator().compare(chi2ndf)
