import pytest

from lazy_object_proxy import Proxy
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.broot import BROOT as br
from spectrum.comparator import Comparator  # noqa

from tools.validate import validate
from vault.datavault import DataVault

PION_INPUT = Proxy(
    lambda:
    (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)

ETA_INPUT = Proxy(
    lambda:
    (
        DataVault().input("single #eta", "low"),
        DataVault().input("single #eta", "high"),
    )
)



# @pytest.mark.skip("TODO: Update me")
@pytest.mark.onlylocal
def test_pi0_efficiency():
    efficiency = evaluate_spmc_efficiency(PION_INPUT, "#pi^{0}")
    # Comparator().compare(efficiency)
    validate(br.hist2dict(efficiency), "spmc_efficiency/#pi^{0}")


@pytest.mark.skip("")
def test_eta_efficiency():
    evaluate_spmc_efficiency(ETA_INPUT, "#eta")


def evaluate_spmc_efficiency(inputs, particle):
    options = CompositeEfficiencyOptions(particle)
    loggs = AnalysisOutput("efficiency_spmc_{}".format(particle))
    efficiency = Efficiency(options).transform(
        inputs,
        loggs
    )
    return efficiency
