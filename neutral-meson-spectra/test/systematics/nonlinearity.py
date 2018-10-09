import unittest

from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityUncertainty
from spectrum.output import AnalysisOutput
from uncertainties.nonlinearity import Nonlinearity, define_inputs
# from vault.datavault import DataVault


# TODO: Look at generated histogram in different selection
#       fix this asap

class TestNonliearityUncertainty(unittest.TestCase):

    def test(self):
        self.nbins = 2
        prod = "single #pi^{0} scan nonlinearity6"
        options = CompositeNonlinearityUncertainty(nbins=self.nbins)
        options.factor = 1.

        chi2ndf = Nonlinearity(options).transform(
            define_inputs(self.nbins, prod),
            loggs=AnalysisOutput("testing the scan interface")
        )
        Comparator().compare(chi2ndf)
