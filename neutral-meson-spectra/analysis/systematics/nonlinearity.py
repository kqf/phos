import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty,
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data


@pytest.fixture
def nbins():
    return 9

# TODO: Look at generated histogram in different selection
#       fix this asap


# Benchmark:
# In the 5 TeV analysis U_nonlin ~ 0.01

@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_nonlinearity_uncertainty(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    options = NonlinearityUncertaintyOptions(nbins=nbins)
    options.factor = 1.

    with open_loggs("nonlinearity uncertainty") as loggs:
        chi2ndf = Nonlinearity(options).transform(
            nonlinearity_scan_data(nbins, prod),
            loggs
        )
    Comparator().compare(chi2ndf)
