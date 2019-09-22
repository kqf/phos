import pytest
from spectrum.spectra import spectrum, data_spectrum
from spectrum.output import open_loggs
from spectrum.comparator import Comparator


@pytest.fixture
def data(particle):
    return data_spectrum(particle=particle)


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}"
])
def test_spectrum(particle, data):
    with open_loggs() as loggs:
        output = spectrum(particle, data, loggs)
        Comparator().compare(output)
