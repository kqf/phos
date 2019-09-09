import pytest

from spectrum.output import open_loggs
from spectrum.comparator import Comparator

from spectrum.uncertainties.nonlinearity import NonlinearityUncertainty
from spectrum.uncertainties.nonlinearity import NonlinearityUncertaintyOptions
from spectrum.uncertainties.nonlinearity import nonlinearity_scan_data
from spectrum.uncertainties.nonlinearity import efficiencies

from spectrum.efficiency import Efficiency
from spectrum.options import CompositeEfficiencyOptions
from spectrum.pipeline import ComparePipeline
from vault.datavault import DataVault


@pytest.fixture
def nbins():
    return 5

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

    with open_loggs() as loggs:
        chi2ndf = NonlinearityUncertainty(options).transform(
            nonlinearity_scan_data(nbins, prod),
            loggs
        )
    Comparator().compare(chi2ndf)


@pytest.mark.skip("This one is used only to check the uncertainties by eyes")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_different_nonlinearities(nbins):
    prod = "single #pi^{0} nonlinearity scan"
    _, data = nonlinearity_scan_data(nbins, prod)
    with open_loggs("nonlinearity uncertainty") as loggs:
        data = efficiencies(data, loggs, nbins=nbins)
        print("Done")
        for i in range(0, len(data), nbins):
            Comparator().compare(data[i: i + nbins])


@pytest.fixture
def spmc_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.fixture
def scan_data():
    prod = "single #pi^{0} nonlinearity scan"
    return (
        DataVault().input(prod, "low", "PhysEff"),
        DataVault().input(prod, "high", "PhysEff"),
    )


@pytest.mark.skip("This one is used only to check the uncertainties by eyes")
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_spmc_efficiency(spmc_data, scan_data):
    options = CompositeEfficiencyOptions("#pi^{0}")
    estimator = ComparePipeline([
        ("spmc", Efficiency(options)),
        ("scan", Efficiency(options)),
    ], plot=True)
    with open_loggs("test") as loggs:
        estimator.transform((spmc_data, scan_data), loggs)
