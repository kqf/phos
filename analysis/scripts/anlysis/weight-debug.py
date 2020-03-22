import ROOT
import pytest

import spectrum.broot as br
from spectrum.pipeline import Pipeline, ComparePipeline
from spectrum.pipeline import HistogramFitter
from spectrum.pipeline import SingleHistReader
from spectrum.pipeline import FunctionTransformer
from spectrum.pipeline import TransformerBase
from spectrum.output import open_loggs

from spectrum.vault import DataVault
from spectrum.vault import FVault


@pytest.fixture
def data():
    return DataVault().input(
        "single #pi^{0}", "low",
        listname="PhysEff", histname="hPt_#pi^{0}_primary_standard")


@pytest.fixture
def compare_data():
    histname = "hPt_#pi^{0}_primary_standard"
    return (
        DataVault().input(
            "single #pi^{0}", "low", listname="PhysEff", histname=histname),
        DataVault().input(
            "single #eta", "low", listname="PhysEff", histname=histname),
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
    estimator = Pipeline([
        ("data", SingleHistReader()),
        ("normalize", FunctionTransformer(br.scalew, no_loggs=True)),
        ("attributes", Attributes()),
        ("fit", HistogramFitter(fitfunc=spectrumf)),
    ])
    with open_loggs("corrected yield #pi{0}") as loggs:
        estimator.transform(data, loggs)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_corrected_different_spectra(compare_data):
    estimator = ComparePipeline([
        ("mcdata", SingleHistReader()),
        ("original", SingleHistReader()),
    ], True)
    with open_loggs() as loggs:
        estimator.transform(compare_data, loggs)
