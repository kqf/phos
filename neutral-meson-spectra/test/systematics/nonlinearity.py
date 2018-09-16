import unittest
from collections import OrderedDict

from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityUncertainty
from spectrum.output import AnalysisOutput
from uncertainties.nonlinearity import Nonlinearity, form_histnames
from vault.datavault import DataVault


# TODO: Look at generated histogram in different selection
#       fix this asap

# TODO: Add Generated Histogram to the nonlinearity scan selection
#

class TestNonliearityUncertainty(unittest.TestCase):

    def test(self):
        self.nbins = 2
        prod = "single #pi^{0} scan nonlinearity6"
        histnames = form_histnames(self.nbins)
        low = DataVault().input(prod, "low", inputs=histnames)
        high = DataVault().input(prod, "high", inputs=histnames)

        unified_inputs = OrderedDict([
            (low, (0.0, 8.0)),
            (high, (4.0, 20.0)),
        ])

        main_inputs = {
            DataVault().input(prod, "low", "PhysEff"): (0.0, 8.0),
            DataVault().input(prod, "high", "PhysEff"): (4.0, 20.0),
        }

        options = CompositeNonlinearityUncertainty(
            unified_inputs, nbins=self.nbins)
        options.factor = 1.

        low, high = low.read_multiple(2), high.read_multiple(2)
        spmc = [(l, h) for l, h in zip(low, high)]

        chi2ndf = Nonlinearity(options).transform(
            (main_inputs, spmc),
            loggs=AnalysisOutput("testing the scan interface")
        )
        Comparator().compare(chi2ndf)
