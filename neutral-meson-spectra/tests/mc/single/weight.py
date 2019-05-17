import ROOT
import pytest  # noqa

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import AnalysisOutput

from vault.datavault import DataVault
from vault.formulas import FVault
from tools.feeddown import data_feeddown


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


def fitfunction():
    tsallis = ROOT.TF1("tsallis", FVault().func("tsallis"), 0, 10)
    tsallis.SetParameters(0.014960701090585591,
                          0.287830380417601,
                          9.921003040859755)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    return tsallis


@pytest.mark.onlylocal
def test_corrected_yield_for_pi0(data):
    options = CompositeCorrectedYieldOptions(particle="#pi^{0}")
    options.fitfunc = fitfunction()
    CorrectedYield(options).transform(
        data,
        loggs=AnalysisOutput("corrected yield #pi^{0}"))
