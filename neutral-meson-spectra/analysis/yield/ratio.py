import pytest

from spectrum.corrected_yield import YieldRatio, CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.output import AnalysisOutput
from spectrum.comparator import Comparator
import spectrum.sutils as su
from tools.feeddown import data_feeddown

from vault.datavault import DataVault


def ratio_input():
    # Define the inputs and the dataset for #eta mesons
    #
    inputs_eta = (
        DataVault().input("single #eta", "low"),
        DataVault().input("single #eta", "high"),
    )

    data_eta = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True),
        ),
        inputs_eta
    )

    options_eta = CompositeCorrectedYieldOptions(particle="#eta")

    # Define the inputs and the dataset for #pi^{0}
    #
    prod = "single #pi^{0}"
    inputs_pi0 = (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )

    data_pi0 = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        inputs_pi0
    )

    options_pi0 = CompositeCorrectedYieldOptions(particle="#pi^{0}")
    # Make same binning for all neutral mesons
    options_pi0.set_binning(
        options_eta.analysis.pt.ptedges,
        options_eta.analysis.pt.rebins
    )
    return data_eta, options_eta, data_pi0, options_pi0


def test_yield_ratio():
    data_eta, options_eta, data_pi0, options_pi0 = ratio_input()

    estimator = YieldRatio(
        options_eta=options_eta,
        options_pi0=options_pi0,
        plot=True
    )

    loggs = AnalysisOutput("eta to pion ratio")
    output = estimator.transform(
        (data_eta, data_pi0),
        loggs=loggs
    )
    Comparator().compare(output)
    loggs.plot()


@pytest.mark.skip('Something is wrong')
def test_debug_ratio():
    data_eta, options_eta, data_pi0, options_pi0 = ratio_input()
    loggs = AnalysisOutput("")
    pi0 = CorrectedYield(options_pi0).transform(data_pi0, loggs)
    eta = CorrectedYield(options_eta).transform(data_eta, loggs)

    su.wait()
    Comparator().compare(eta, pi0)
