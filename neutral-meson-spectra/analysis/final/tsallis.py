import ROOT
import pytest  # noqa

from spectrum.spectra import spectrum
# from spectrum.comparator import Comparator
from spectrum.constants import mass
from spectrum.plotter import plot
from vault.formulas import FVault


@pytest.fixture
def tsallisf(particle):
    tsallis = FVault().tf1("tsallis")
    if particle == "#pi^{0}":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.125)
        tsallis.SetParLimits(1, 0.100, 0.300)
        tsallis.FixParameter(2, 6.500)
        tsallis.SetParLimits(2, 6.000, 8.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(1.4, 20)

    if particle == "#eta":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.238)
        tsallis.SetParLimits(1, 0.200, 0.300)
        tsallis.SetParameter(2, 6.19)
        tsallis.SetParLimits(2, 5.5, 7.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(2.2, 20)

    tsallis.FixParameter(3, mass(particle))
    tsallis.FixParameter(4, mass(particle))
    tsallis.SetTitle("Tsallis function")
    tsallis.SetLineColor(ROOT.kBlue + 1)
    tsallis.SetNpx(100)
    return tsallis


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_tsallis_fit(particle, tsallisf):
    cyield = spectrum(particle)
    cyield.SetTitle("{} yield".format(particle))
    cyield.Fit(tsallisf, "R")
    tsallisf.SetRange(0.6, 21)
    plot([cyield, tsallisf])
