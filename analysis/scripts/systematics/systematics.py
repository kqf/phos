import pytest
import spectrum.broot as br
from spectrum.uncertainties.total import data_total_uncert
from spectrum.uncertainties.total import TotalUncertainty
from spectrum.uncertainties.total import TotalUncertaintyOptions
from spectrum.output import open_loggs

from spectrum.comparator import Comparator


@pytest.fixture
def dataset(particle):
    return data_total_uncert(particle)


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_calculates_total_uncertainty(particle, dataset, stop):
    with open_loggs() as loggs:
        estimator = TotalUncertainty(
            TotalUncertaintyOptions(particle=particle),
            plot=stop
        )
        tot = estimator.transform(dataset, loggs)
        print()
        print(
            "\def \{}MeanTotalUncertainty {{{:.2f}}}".format(
                br.spell(particle),
                br.bins(tot).contents.mean() * 100
            )
        )
        Comparator().compare(tot)
