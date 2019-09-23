import pytest
from spectrum.spectra import spectrum
from spectrum.comparator import Comparator
from spectrum.pipeline import RebinTransformer
from spectrum.broot import BROOT as br

from spectrum.output import open_loggs


@pytest.mark.thesis
@pytest.mark.onlylocal
def test_spectrum():
    pion, _, _ = spectrum("#pi^{0}")
    eta, _, _ = spectrum("#eta")
    eta.logy = True
    eta.logx = True
    eta.label = "#eta"
    eta.label = "#pi^{0}"
    with open_loggs() as loggs:
        pion = RebinTransformer(True, br.edges(eta)).transform(pion, loggs)
    eta_pion = Comparator().compare(eta, pion)
    Comparator().compare(eta_pion)
