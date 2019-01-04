import pytest

from spectrum.output import AnalysisOutput
from spectrum.pipeline import ComparePipeline
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.options import CompositeNonlinearityUncertainty
from tools.feeddown import data_feeddown
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
    production = "single #pi^{0}"
    spmc_inputs = (
        DataVault().input(production, "low", "PhysEff"),
        DataVault().input(production, "high", "PhysEff"),
    )

    cyield = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        spmc_inputs
    )

    tof = (
        DataVault().input("data", histname="MassPtSM0"),
        DataVault().input("data", "isolated", histname="MassPtSM0"),
    )

    gscale = (
        (
            ep_data("data"),
            ep_data("pythia8", "ep_ratio_1"),
        ),
        cyield,
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
        define_inputs(nbins, "single #pi^{0}"),
        tof,
        gscale,
        acceptance,
    )


@pytest.mark.interactive
@pytest.mark.onlylocal
def test_draws_all_sources():
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
