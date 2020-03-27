from __future__ import print_function
import pytest

import spectrum.broot as br
from spectrum.output import open_loggs
from spectrum.options import CompositeEfficiencyOptions
from spectrum.efficiency import PeakPositionWidthEstimator
from spectrum.efficiency import efficiency_data
from spectrum.comparator import Comparator


@pytest.fixture
def data():
    return efficiency_data()


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_pt_ranges(data, stop=False):
    estimator = PeakPositionWidthEstimator(
        CompositeEfficiencyOptions("#pi^{0}")
    )
    with open_loggs() as loggs:
        mass, massf, width, widthf = estimator._estimate(data, loggs)
        Comparator(stop=stop).compare(mass)
        print(br.pars(massf))
