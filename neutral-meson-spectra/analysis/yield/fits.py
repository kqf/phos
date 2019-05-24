import ROOT
import pytest  # noqa

from lazy_object_proxy import Proxy
from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.comparator import Comparator

from vault.datavault import DataVault
from tools.feeddown import data_feeddown
from vault.formulas import FVault


@pytest.fixture
def tsallisf():
    tsallis = ROOT.TF1("tsallis", FVault().func("tsallis"), 0, 10)
    tsallis.SetParameters(0.014960701090585591,
                          0.287830380417601,
                          9.921003040859755)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    return tsallis


@pytest.fixture
def tcmf():
    tcm = ROOT.TF1("tcm", FVault().func("tcm"), 0, 10)
    tcm.SetParameters(
        0.1,
        4.35526e-01,
        8.02315e-01,
        9.20052e-01)
    return tcm


PION_INPUTS = Proxy(
    lambda:
    (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )
)
ETA_INPUTS = Proxy(
    lambda:
    (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(dummy=True)
        ),
        (
            DataVault().input("single #eta", "low"),
            DataVault().input("single #eta", "high"),
        )
    )
)


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.skip("Don't something is wrong with tcm formula")
@pytest.mark.parametrize("particle, data", [
    ("#pi^{0}", PION_INPUTS),
    # ("#eta", ETA_INPUTS),
])
def test_tsallis_fit(particle, data, tsallisf):
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle=particle)
    )
    cyield = estimator.transform(data, loggs={})
    cyield.Fit(tsallisf)
    cyield.logy = True
    cyield.logx = True
    Comparator().compare(cyield)


# @pytest.mark.skip("Don't something is wrong with tcm formula")
@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle, data", [
    ("#pi^{0}", PION_INPUTS),
    # ("#eta", ETA_INPUTS),
])
def test_tcm_fit(particle, data, tcmf):
    estimator = CorrectedYield(
        CompositeCorrectedYieldOptions(particle=particle)
    )
    cyield = estimator.transform(data, loggs={})
    cyield.Fit(tcmf)
    cyield.logy = True
    cyield.logx = True
    Comparator().compare(cyield)
