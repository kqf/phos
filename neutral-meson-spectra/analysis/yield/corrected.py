import pytest  # noqa

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield, data_cyield
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
from spectrum.constants import PARTICLE_MASSES
from vault.formulas import FVault


@pytest.fixture
def data(particle):
    return data_cyield(particle)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    # "#eta",
])
def test_fit_the_corrected_yield(particle, data):
    with open_loggs() as loggs:
        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(
                particle=particle
            )
        )
        cyield = estimator.transform(data, loggs)
        tsallis = FVault().tf1("tsallis")
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.135)
        tsallis.SetParLimits(1, 0.100, 0.300)
        tsallis.FixParameter(2, 6.500)
        tsallis.SetParLimits(2, 6.000, 7.000)
        tsallis.FixParameter(3, PARTICLE_MASSES[particle])
        cyield.Fit(tsallis)
        Comparator().compare(cyield)
