import pytest
import ROOT

# import spectrum.broot as br
from spectrum.pipeline import SingleHistReader
from spectrum.output import open_loggs
# from spectrum.comparator import Comparator
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.pipeline import TransformerBase
from spectrum.analysis import Analysis

from spectrum.options import Options

from vault.datavault import DataVault
from vault.formulas import FVault


class IdentityTransform(object):
    def transform(self, inputs, loggs):
        return inputs.GetHistogram()


@pytest.fixture
def tsallis():
    tsallis = ROOT.TF1("f", FVault().func("tsallis"), 0, 100)
    tsallis.SetParameters(
        0.0149,
        0.2878,
        9.9210)
    tsallis.FixParameter(3, 0.135)
    tsallis.FixParameter(4, 0.135)
    tsallis.label = "tsallis"
    return tsallis


class GeneratedValidator(TransformerBase):
    def __init__(self):
        super(GeneratedValidator, self).__init__()
        self.pipeline = ComparePipeline([
            ("hist", SingleHistReader()),
            ("func", IdentityTransform())
        ], plot=True)


class ReconstructedValidator(TransformerBase):
    def __init__(self, func, options=Options()):
        super(ReconstructedValidator, self).__init__()
        nmesons = Pipeline([
            ("ReconstructMesons", Analysis(options)),
            ("NumberOfMesons", HistogramSelector("nmesons"))
        ])
        self.pipeline = ComparePipeline([
            ("nmesons", nmesons),
            ("func", IdentityTransform())
        ], plot=True)


@pytest.fixture
def data(tsallis, estimator):
    histname = "hPt_#pi^{0}_primary_standard"
    if type(estimator) == ReconstructedValidator:
        histname = "MassPt"

    return (
        DataVault().input("single #pi^{0}", "high",
                          listname="PhysEff", histname=histname),
        tsallis
    )


@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("estimator", [
    ReconstructedValidator(Options(particle="#pi^{0}")),
    GeneratedValidator(),
])
def test_spectra(data, estimator):
    with open_loggs() as loggs:
        estimator.transform(data, loggs)
