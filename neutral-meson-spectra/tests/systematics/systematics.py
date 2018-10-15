import unittest

from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline
from spectrum.options import CompositeNonlinearityUncertainty
from uncertainties.yields import YieldExtractioin
from uncertainties.nonlinearity import Nonlinearity, define_inputs
from tests.uncertainties.yields import YieldExtractioinUncertanityOptions
from vault.datavault import DataVault


def data(nbins):
    production = "single #pi^{0} iteration d3 nonlin14"
    yields_inputs = (
        DataVault().input(production, "low"),
        DataVault().input(production, "high"),
    )

    yields = (
        DataVault().input("data"),
        yields_inputs
    )
    return (
        yields,
        define_inputs(nbins),
    )


class DrawAllSources(unittest.TestCase):

    def test_all(self):
        nbins = 2
        nonlin_options = CompositeNonlinearityUncertainty(nbins=nbins)
        nonlin_options.factor = 1.

        estimator = ComparePipeline((
            ("yield", YieldExtractioin(YieldExtractioinUncertanityOptions())),
            ("nonlinearity", Nonlinearity(nonlin_options)),
        ))
        estimator.transform(
            data(nbins),
            loggs=AnalysisOutput("testing the scan interface")
        )
