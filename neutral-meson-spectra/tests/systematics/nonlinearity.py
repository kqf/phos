import pytest

from spectrum.comparator import Comparator
from spectrum.output import AnalysisOutput

from uncertainties.nonlinearity import Nonlinearity, nonlinearity_scan_data
from uncertainties.nonlinearity import CompositeNonlinearityUncertaintyOptions


# TODO: Look at generated histogram in different selection
#       fix this asap

@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_nonlinearity_uncertainty():
    nbins = 2
    prod = "single #pi^{0} nonlinearity scan"
    options = CompositeNonlinearityUncertaintyOptions(nbins=nbins)
    options.factor = 1.

    chi2ndf = Nonlinearity(options).transform(
        nonlinearity_scan_data(nbins, prod),
        loggs=AnalysisOutput("testing the scan interface")
    )
    Comparator().compare(chi2ndf)
