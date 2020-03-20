import ROOT
import pytest  # noqa

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.cyield import CorrectedYield
from spectrum.output import open_loggs

from spectrum.vault import DataVault
from spectrum.vault import FVault
from spectrum.tools.feeddown import data_feeddown


@pytest.fixture
def data():
    return (
        (
            DataVault().input("data", listname="Phys", histname="MassPtSM0"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )


@pytest.fixture
def yieldf():
    tsallis = ROOT.TF1("tsallis", FVault().func("tsallis"), 0.8, 10)
    tsallis.SetParameters(0.015, 0.288, 9.921)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    return tsallis


@pytest.mark.onlylocal
def test_corrected_yield_for_pi0(data, yieldf):
    options = CompositeCorrectedYieldOptions(particle="#pi^{0}")
    options.fitfunc = yieldf
    with open_loggs() as loggs:
        CorrectedYield(options).transform(data, loggs)
