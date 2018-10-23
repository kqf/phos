import unittest

from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CompositeNonlinearityUncertainty
from uncertainties.yields import YieldExtractioin
from uncertainties.yields import YieldExtractioinUncertanityOptions
from uncertainties.nonlinearity import Nonlinearity, define_inputs
from uncertainties.tof import TofUncertainty, TofUncertaintyOptions
from uncertainties.gscale import GScale, GScaleOptions
from uncertainties.acceptance import Acceptance, AcceptanceOptions
from vault.datavault import DataVault


def ep_data(prod="data", version="ep_ratio"):
    return DataVault().input(
        prod,
        version=version,
        listname="PHOSEpRatioCoutput1",
        histname="Ep_ele",
        use_mixing=False)


def data(nbins):
    production = "single #pi^{0} iteration d3 nonlin14"
    spmc_inputs = (
        DataVault().input(production, "low"),
        DataVault().input(production, "high"),
    )

    cyield = (
        DataVault().input("data"),
        spmc_inputs
    )

    tof = (
        DataVault().input("data"),
        DataVault().input("data", "isolated", histname="MassPtSM0"),
    )

    gscale = (
        (
            ep_data("data"),
            ep_data("pythia8", "ep_ratio_1"),
        ),
        (
            DataVault().input("data"),
            spmc_inputs
        ),
    )

    acceptance = (
        cyield,  # Original corrected yield data
        (
            cyield,  # 1 cm distance to a bad cell
            cyield,  # 2 cm distance to a bad cell
        )
    )

    return (
        cyield,
        define_inputs(nbins, "single #pi^{0} scan nonlinearity6"),
        tof,
        gscale,
        acceptance,
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
            ("gescale", GScale(GScaleOptions(particle="#pi^{0}"))),
            ("accepntace", Acceptance(AcceptanceOptions(particle="#pi^{0}"))),
        ), plot=True)

        loggs = AnalysisOutput("testing the scan interface")
        estimator.transform(data(nbins), loggs)
        loggs.plot(True)
