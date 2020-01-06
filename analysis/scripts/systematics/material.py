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
# Inherits from previous analyses

@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_material_budget(particle, data):
    material = MaterialBudget(MaterialBudgetOptions(particle=particle))
    with open_loggs() as loggs:
        output = material.transform(data, loggs)
        Comparator().compare(output)
