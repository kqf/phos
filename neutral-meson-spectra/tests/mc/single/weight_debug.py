import ROOT
import pytest

from lazy_object_proxy import Proxy
from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.pipeline import OutputFitter
from spectrum.input import SingleHistInput
from spectrum.options import Options
from spectrum.output import AnalysisOutput
from spectrum.pipeline import TransformerBase
# from spectrum.comparator import Comparator
# from spectrum.broot import BROOT as br

from vault.datavault import DataVault
from vault.formulas import FVault

DATASET = Proxy(
    lambda: DataVault().input("single #pi^{0}", "low", listname="PhysEff")
)

# NB: This dataset is now obsolete
COMPARE_DATASETS = Proxy(
    lambda:
    (
        DataVault().input("single #pi^{0}", "low", listname="PhysEff"),
        DataVault().input("single alternative", "low", listname="PhysEff"),
    )
)


class Attributes(TransformerBase):
    def transform(self, data, loggs):
        data.logy = True
        data.logx = True
        return data


def fitfunc():
    tsallis = ROOT.TF1(
        "tsallis",
        FVault().func("tsallis", "standard"), 0, 8)

    parameters = [0.2622666606436988,
                  0.08435275173194286,
                  7.356520553419461]

    for i, par in enumerate(parameters):
        tsallis.FixParameter(i, par)
    # tsallis.SetParameter(0, parameters[0])

    # tsallis.SetParameters(0.014960701090585591,
    # 0.287830380417601, 9.921003040859755)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    return tsallis


def test_corrected_yield_for_pi0():
    options = Options()
    options.fitfunc = fitfunc()
    estimator = Pipeline([
        ("data", SingleHistInput(
            "hPt_#pi^{0}_primary_standard", norm=True)),
        ("attributes", Attributes()),
        ("fit", OutputFitter(options)),
    ])

    estimator.transform(DATASET, AnalysisOutput("corrected yield #pi^{0}"))


@pytest.mark.skip('Obsolete dataset')
def test_corrected_different_spectra():
    estimator = ComparePipeline([
        ("mcdata", SingleHistInput(
            "hPt_#pi^{0}_primary_standard", norm=False)),
        ("original", SingleHistInput(
            "hPt_#pi^{0}_primary_standard", norm=False)),
    ], True)
    estimator.transform(
        COMPARE_DATASETS,
        AnalysisOutput("corrected yield #pi^{0}"))
