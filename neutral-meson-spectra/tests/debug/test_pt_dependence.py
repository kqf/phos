import pytest
from spectrum.options import CompositeEfficiencyOptions
from spectrum.output import AnalysisOutput
from spectrum.efficiency import PeakPositionWidthEstimator
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


@pytest.mark.onlyocal
@pytest.mark.interactive
def test_pt_ranges():
    inputs = (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )

    estimator = PeakPositionWidthEstimator(
        CompositeEfficiencyOptions("#pi^{0}")
    )
    loggs = AnalysisOutput("test ranges")
    mass, massf, width, widthf = estimator._estimate(inputs, loggs)
    # loggs.plot()
    Comparator().compare(mass)
    # Comparator().compare(width)
    print br.pars(massf)
