import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.input import read_histogram
from spectrum.comparator import Comparator
from vault.datavault import DataVault


@pytest.fixture
def data(particle, region):
    return DataVault().input(
        "single {}".foramt(particle),
        region,
        "PhysEff", label="{} p_{{T}}".format(region)
    )


@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
@pytest.mark.parametrize("region", ["low", "high"])
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
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
@pytest.mark.parametrize("region", ["low", "high"])
def test_reconstructed(particle, data):
    Comparator().compare(reconstructed(particle, data))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
@pytest.mark.parametrize("region", ["low", "high"])
@pytest.mark.parametrize("quantity", [
    "hEtaPhi_{0}",
    "hPt_{0}_primary_",
])
def test_distribution(particle, region, data, quantity):
    hist = data.read_single(quantity.format(particle), norm=True)
    if "_primary_" in quantity:
        hist.logy = True
    Comparator().compare(hist)
