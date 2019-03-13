import pytest
from lazy_object_proxy import Proxy

from spectrum.output import AnalysisOutput
from spectrum.options import CompositeEfficiencyOptions
from spectrum.efficiency import PeakPositionWidthEstimator
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault

DATASET = Proxy(
    lambda x: (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )
)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_pt_ranges():
    estimator = PeakPositionWidthEstimator(
        CompositeEfficiencyOptions("#pi^{0}")
    )
    loggs = AnalysisOutput("test ranges")
    mass, massf, width, widthf = estimator._estimate(DATASET, loggs)
    # loggs.plot()
    Comparator().compare(mass)
    # Comparator().compare(width)
    print br.pars(massf)
