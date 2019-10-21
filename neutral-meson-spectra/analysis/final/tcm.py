import pytest  # noqa

from spectrum.spectra import spectrum
from spectrum.comparator import Comparator
from spectrum.constants import mass
from vault.formulas import FVault


@pytest.fixture
def tcmf(particle):
    tcm = FVault().tf1("tcm", "{} 13 TeV".format(particle))

    if particle == "#pi^{0}":
        tcm.SetParameter(0, 0.1)
        tcm.SetParameter(1, 1.73e-01)
        tcm.SetParLimits(1, 0.1, 0.3)
        tcm.SetParameter(2, 0.1)
        tcm.SetParameter(3, 0.601)
        tcm.SetParLimits(3, 0.4, 1.0)
        tcm.SetParameter(4, 3.09)
        tcm.SetParLimits(4, 2.0, 4.0)

    if particle == "#eta":
        # pass
        tcm.SetParameter(0, 0.1)
        tcm.SetParLimits(0, 0, 1e4)
        tcm.SetParameter(1, 1.71e-01)
        tcm.SetParLimits(1, 0.1, 0.3)
        tcm.SetParameter(2, 0.1)
        tcm.SetParameter(3, 0.801)
        # tcm.SetParLimits(3, 0.7, 0.9)
        tcm.SetParameter(4, 3.059)
        # tcm.SetParLimits(4, 2.0, 4.0)

    tcm.FixParameter(5, mass(particle))
    return tcm


# @pytest.mark.skip("Don't something is wrong with tcm formula")
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    # "#pi^{0}",
    "#eta",
])
def test_tcm_fit(particle, tcmf):
    cyield = spectrum(particle)
    cyield.SetTitle("final yield")
    cyield.Fit(tcmf, "R")
    cyield.logy = True
    cyield.logx = True
    Comparator().compare(cyield)
