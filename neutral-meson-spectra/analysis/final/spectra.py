import pytest
from spectrum.spectra import spectrum
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_spectrum(particle):
    output = spectrum(particle)
    Comparator().compare(output)
