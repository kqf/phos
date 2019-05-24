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


@pytest.mark.interactive
@pytest.mark.parametrize("data, particle", [
    (PION_INPUTS, "#pi^{0}"),
    # (ETA_INPUTS, "#eta"),
])
def test_corrected_yield_for_pi0(data, particle):
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(
            particle=particle
        )
    )
    loggs = AnalysisOutput("corrected yield {}".format(particle))
    estimator.transform(data, loggs=loggs)
    loggs.plot()
