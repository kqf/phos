import pytest

from spectrum.comparator import Comparator
from spectrum.options import CompositeNonlinearityUncertainty
from spectrum.output import AnalysisOutput
from uncertainties.nonlinearity import Nonlinearity, define_inputs
# from vault.datavault import DataVault


# TODO: Look at generated histogram in different selection
#       fix this asap

@pytest.mark.thesis
@pytest.mark.interactive
@pytest.mark.onlylocal
def test_nonlinearity_uncertainty():
    nbins = 2
    prod = "single #pi^{0}"
    options = CompositeNonlinearityUncertainty(nbins=nbins)
    options.factor = 1.

    chi2ndf = Nonlinearity(options).transform(
        define_inputs(nbins, prod),
        loggs=AnalysisOutput("testing the scan interface")
    )
    Comparator().compare(chi2ndf)
