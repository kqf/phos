import pytest
from spectrum.spectra import ratio
from spectrum.comparator import Comparator


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_spectrum():
    Comparator().compare(ratio(True))
