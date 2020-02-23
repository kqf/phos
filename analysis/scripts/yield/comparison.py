import pytest

from spectrum.output import open_loggs
from spectrum.analysis import Analysis
from spectrum.tools.feeddown import data_feeddown
from spectrum.options import Options
from spectrum.cyield import CorrectedYield
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.comparator import Comparator


@pytest.fixture
def yield_data(data, particle):
    use_dummy = particle != "#pi^{0}"
    return data, data_feeddown(dummy=use_dummy)


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_simple(particle, spmc, data, yield_data, stop):
    with open_loggs() as loggs:
        estimator = Analysis(Options(particle=particle))
        raw_yield = estimator.transform(data, loggs).spectrum

        estimator = Efficiency(CompositeEfficiencyOptions(particle=particle))
        efficiency = estimator.transform(spmc, loggs)

        estimator = CorrectedYield(
            CompositeCorrectedYieldOptions(particle=particle)
        )
        corr_yield = estimator.transform((yield_data, spmc), loggs)
        print([raw_yield, efficiency, corr_yield])
        Comparator(stop=stop).compare([raw_yield, efficiency, corr_yield])
