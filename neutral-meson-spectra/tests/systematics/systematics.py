import unittest

from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CompositeNonlinearityUncertainty
from uncertainties.yields import YieldExtractioin
from uncertainties.yields import YieldExtractioinUncertanityOptions
from uncertainties.nonlinearity import Nonlinearity, define_inputs
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
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

    tof = (
        DataVault().input("data"),
        DataVault().input("data"),
    )
    return (
        yields,
        define_inputs(nbins, "single #pi^{0} scan nonlinearity6"),
        tof,
    )


class DrawAllSources(unittest.TestCase):

    def test_all(self):
        nbins = 2
        nonlin_options = CompositeNonlinearityUncertainty(nbins=nbins)
        nonlin_options.factor = 1.

        cyield_options = CompositeCorrectedYieldOptions(particle="#pi^{0}")

        estimator = ComparePipeline((
            ("yield", YieldExtractioin(
                YieldExtractioinUncertanityOptions(cyield_options))),
            ("nonlinearity", Nonlinearity(nonlin_options)),
            ("tof", TofUncertainty(TofUncertaintyOptions())),
        ), plot=True)
        loggs = AnalysisOutput("testing the scan interface")
        estimator.transform(
            data(nbins),
            loggs
        )
        loggs.plot(True)
