import pytest
from spectrum.input import read_histogram
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


@pytest.mark.onlylocal
def test_draw_generated_spectra():
    pi0 = read_histogram(DataVault().file("single #pi^{0}", "low"),
                         "PhysEff", "hPtLong_#pi^{0}", "#pi^{0}")

    eta = read_histogram(DataVault().file("single #eta", "low"),
                         "PhysEff", "hPtLong_#eta", "#eta")

    for e in (eta, pi0):
        br.scalew(e, 1. / e.Integral())
        e.logx = True
        e.logy = True
        e.SetAxisRange(0, 10, "X")

    diff = Comparator(rrange=(0.8, 1.2))
    diff.compare(eta, pi0)
