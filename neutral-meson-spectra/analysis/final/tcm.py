import pytest  # noqa

from spectrum.spectra import spectrum
from spectrum.comparator import Comparator
from spectrum.constants import mass
from vault.formulas import FVault


@pytest.fixture
def tcmf(particle):
    tcm = FVault().tf1("tcm")
    tcm.SetParameters(0.1, 4.35526e-01, 8.02315e-01, 9.20052e-01, 1)
    tcm.FixParameter(6, mass(particle))
    return tcm


# @pytest.mark.skip("Don't something is wrong with tcm formula")
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_tcm_fit(particle, tcmf):
    cyield, _, _ = spectrum(particle)
    cyield.SetTitle("final yield")
    cyield.Fit(tcmf)
    cyield.logy = True
    cyield.logx = True
    Comparator().compare(cyield)
