import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator  # noqa

from spectrum.uncertainties.material import MaterialBudget
from spectrum.uncertainties.material import MaterialBudgetOptions
from spectrum.uncertainties.material import material_budget_data


@pytest.fixture
def data():
    return material_budget_data()


# Benchmark:
# In the 5 TeV analysis U_tof ~ 0.02

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_tof(particle, data):
    tof = MaterialBudget(MaterialBudgetOptions(particle=particle))
    with open_loggs() as loggs:
        output = tof.transform(data, loggs)
        Comparator().compare(output)
    assert len(output) > 0
