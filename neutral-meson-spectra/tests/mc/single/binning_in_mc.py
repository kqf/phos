import pytest
import ROOT

from spectrum.input import SingleHistInput
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
from spectrum.pipeline import ComparePipeline, Pipeline, HistogramSelector
from spectrum.analysis import Analysis

from spectrum.options import Options

from vault.datavault import DataVault
from vault.formulas import FVault


class FunctionOutput(object):

    def __init__(self, func):
        super(FunctionOutput, self).__init__()
        self.func = func

    def transform(self, inputs, loggs):
        return self.func


class ReconstructedValidator(object):
    def __init__(self, func, options=Options()):
        super(ReconstructedValidator, self).__init__()
        nmesons = Pipeline([
            ("ReconstructMesons", Analysis(options)),
            ("NumberOfMesons", HistogramSelector("nmesons"))
        ])
        self.runion = ComparePipeline([
            ("nmesons", nmesons),
            ("func", FunctionOutput(func))
        ])


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


class GeneratedValidator(object):
    def __init__(self, func, histname):
        super(GeneratedValidator, self).__init__()
        self.runion = ComparePipeline([
            ("hist", SingleHistInput(histname)),
            ("func", FunctionOutput(func))
        ])


@pytest.fixture
def data():
    return (
        DataVault().input("single #pi^{0}", "high", listname="PhysEff"),
        None
    )


@pytest.mark.onlylocal
def test_pi0_reconstructed(data, tsallis):
    estimator = ReconstructedValidator(tsallis, Options(particle="#pi^{0}"))

    with open_loggs("extraction spmc {}".format("#pi^{0}")) as loggs:
        output = estimator.transform(data, loggs)
        output.logy = False
        diff = Comparator(stop=True, crange=(0, 8000))
        diff.compare(output)


@pytest.mark.onlylocal
def test_pi0_generated(data, tsallis):
    estimator = GeneratedValidator(tsallis, "hPt_#pi^{0}_primary_standard")

    with open_loggs("spectrum extraction spmc {}".format("#pi^{0}")) as loggs:
        output = estimator.transform(data, loggs)
        output.logy = False
        diff = Comparator(stop=True)
        diff.compare(output)
