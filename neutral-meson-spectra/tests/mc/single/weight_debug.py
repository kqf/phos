import ROOT
import pytest

from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.pipeline import OutputFitter
from spectrum.input import SingleHistInput
from spectrum.options import Options
from spectrum.pipeline import TransformerBase
from spectrum.output import open_loggs
# from spectrum.comparator import Comparator
# from spectrum.broot import BROOT as br

from vault.datavault import DataVault
from vault.formulas import FVault


@pytest.fixture
def data():
    return DataVault().input("single #pi^{0}", "low", listname="PhysEff")


@pytest.fixture
def compare_data():
    return (
        DataVault().input("single #pi^{0}", "low", listname="PhysEff"),
        DataVault().input("single #eta", "low", listname="PhysEff"),
    )


class Attributes(TransformerBase):
    def transform(self, data, loggs):
        data.logy = True
        data.logx = True
        return data


@pytest.fixture
def spectrumf():
    tsallis = ROOT.TF1(
        "tsallis",
        FVault().func("tsallis", "standard"), 0, 8)

    parameters = [0.260, 0.085, 7.372]
    for i, par in enumerate(parameters):
        tsallis.FixParameter(i, par)
    # tsallis.SetParameter(0, parameters[0])
    # tsallis.SetParameters(0.014960701090585591,
    # 0.287830380417601, 9.921003040859755)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    return tsallis


@pytest.mark.onlylocal
def test_corrected_yield_for_pi0(data, spectrumf):
    options = Options()
    options.fitfunc = spectrumf
    estimator = Pipeline([
        ("data", SingleHistInput(
            "hPt_#pi^{0}_primary_standard", norm=True)),
        ("attributes", Attributes()),
        ("fit", OutputFitter(options)),
    ])

    with open_loggs("corrected yield #pi{0}") as loggs:
        estimator.transform(data, loggs)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_corrected_different_spectra(compare_data):
    estimator = ComparePipeline([
        ("mcdata", SingleHistInput(
            "hPt_#pi^{0}_primary_standard", norm=False)),
        ("original", SingleHistInput(
            "hPt_#pi^{0}_primary_standard", norm=False)),
    ], True)
    with open_loggs("corrected yield #pi^{0}") as loggs:
        estimator.transform(compare_data, loggs)
