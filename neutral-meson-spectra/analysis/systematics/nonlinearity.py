import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data
from spectrum.uncertainties.nonlinearity import efficiencies


@pytest.fixture
def nbins():
    return 9

# TODO: Look at generated histogram in different selection
#       fix this asap


# Benchmark:
# In the 5 TeV analysis U_nonlin ~ 0.01

@pytest.mark.skip()
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_nonlinearity_uncertainty(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    options = NonlinearityUncertaintyOptions(nbins=nbins)
    options.factor = 1.

    with open_loggs("nonlinearity uncertainty") as loggs:
        chi2ndf = NonlinearityUncertainty(options).transform(
            nonlinearity_scan_data(nbins, prod),
            loggs
        )
    Comparator().compare(chi2ndf)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_different_nonlinearities(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    _, data = nonlinearity_scan_data(nbins, prod)
    with open_loggs("nonlinearity uncertainty") as loggs:
        data = efficiencies(data, loggs, nbins=nbins)
        for i in range(0, len(data), nbins):
            Comparator().compare(data[i: i + nbins])
