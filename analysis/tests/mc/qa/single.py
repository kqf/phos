import pytest

from spectrum.analysis import Analysis
from spectrum.options import Options
from spectrum.comparator import Comparator
from spectrum.vault import DataVault


@pytest.fixture
def data(particle, region):
    return DataVault().input(
        "single {}".format(particle),
        region,
        "PhysEff", label="{} #it{{p}}_{{T}}".format(region)
    )


@pytest.mark.skip
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
@pytest.mark.parametrize("region", ["low", "high"])
def reconstructed(particle, data):
    reconstructed = Analysis(Options(particle=particle)).transform(data, {})
    reconstructed = reconstructed.spectrum
    reconstructed.SetTitle(reconstructed.GetTitle())
    # br.scalew(reconstructed)
    return reconstructed


@pytest.mark.skip
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", ["#pi^{0}", "#eta"])
@pytest.mark.parametrize("region", ["low", "high"])
def test_reconstructed(particle, data):
    Comparator().compare(reconstructed(particle, data))
