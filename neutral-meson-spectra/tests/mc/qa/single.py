import pytest

from lazy_object_proxy import Proxy
from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.input import read_histogram
from spectrum.comparator import Comparator
from vault.datavault import DataVault


# TODO: Add to thesis images
INPUTS = (
    ("#pi^{0}", Proxy(
        lambda: DataVault().input("single #pi^{0}", "low",
                                  "PhysEff", label="low p_{T}")
    )),

    ("#pi^{0}", Proxy(
        lambda: DataVault().input("single #pi^{0}", "high",
                                  "PhysEff", label="high p_{T}")
    )),

    ("#eta", Proxy(
        lambda: DataVault().input("single #eta", "low",
                                  "PhysEff", label="low p_{T}")
    )),

    ("#eta", Proxy(
        lambda: DataVault().input("single #eta", "high",
                                  "PhysEff", label="high p_{T}")
    )),
)


@pytest.mark.parametrize("particle, data", INPUTS)
def reconstructed(particle, data):
    if "gamma" in particle:
        reconstructed = read_histogram(*data)
        reconstructed.SetTitle("Inclusive " + reconstructed.GetTitle().lower())
        return reconstructed

    reconstructed = Analysis(Options(particle=particle)).transform(data, {})
    reconstructed = reconstructed.spectrum
    reconstructed.SetTitle(reconstructed.GetTitle())
    # br.scalew(reconstructed)
    return reconstructed


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle, data", INPUTS)
def test_reconstructed(particle, data):
    Comparator().compare(reconstructed(particle, data))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle, data", INPUTS)
@pytest.mark.parametrize("quantity", [
    "hEtaPhi_{0}",
    "hPt_{0}_primary_",
])
def test_distribution(particle, data, quantity):
    hist = data.read_single(quantity.format(particle), norm=True)
    if "_primary_" in quantity:
        hist.logy = True
    Comparator().compare(hist)
