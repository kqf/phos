import pytest  # noqa
from lazy_object_proxy import Proxy
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault
from tools.feeddown import data_feeddown

PION_INPUTS = Proxy(
    lambda:
    (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )
)
ETA_INPUTS = Proxy(
    lambda:
    (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True)
        ),
        (
            DataVault().input("single #eta", "low"),
            DataVault().input("single #eta", "high"),
        )
    )
)


@pytest.mark.skip("")
def test_corrected_yield_for_pi0():
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(
            particle="#pi^{0}"
        )
    )
    estimator.transform(
        PION_INPUTS,
        loggs=AnalysisOutput("corrected yield #pi^{0}"))


def test_corrected_yield_for_eta():
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle="#eta")
    )
    estimator.transform(
        ETA_INPUTS,
        loggs=AnalysisOutput("corrected yield #eta")
    )
