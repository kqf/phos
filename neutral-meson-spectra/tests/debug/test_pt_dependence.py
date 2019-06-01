from __future__ import print_function
import pytest

from spectrum.output import open_loggs
from spectrum.options import CompositeEfficiencyOptions
from spectrum.efficiency import PeakPositionWidthEstimator
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


@pytest.fixture
def data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_pt_ranges(data):
    estimator = PeakPositionWidthEstimator(
        CompositeEfficiencyOptions("#pi^{0}")
    )
    with open_loggs("test ranges") as loggs:
        mass, massf, width, widthf = estimator._estimate(data, loggs)
        Comparator().compare(mass)
        # Comparator().compare(width)
        print(br.pars(massf))
