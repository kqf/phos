import pytest

from spectrum.comparator import Comparator
from spectrum.output import open_loggs

from uncertainties.nonlinearity import Nonlinearity, nonlinearity_scan_data
from uncertainties.nonlinearity import CompositeNonlinearityUncertaintyOptions


@pytest.fixture
def nbins():
    return 9

# TODO: Look at generated histogram in different selection
#       fix this asap


@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_nonlinearity_uncertainty(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    options = CompositeNonlinearityUncertaintyOptions(nbins=nbins)
    options.factor = 1.

    with open_loggs("nonlinearity uncertainty") as loggs:
        chi2ndf = Nonlinearity(options).transform(
            nonlinearity_scan_data(nbins, prod),
            loggs
        )
    Comparator().compare(chi2ndf)
