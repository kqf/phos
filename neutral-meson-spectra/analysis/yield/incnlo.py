import pytest

from spectrum.options import CompositeCorrectedYieldOptions
from spectrum.corrected_yield import CorrectedYield
from spectrum.output import open_loggs
from spectrum.pipeline import ComparePipeline, Pipeline
from spectrum.pipeline import FunctionTransformer
from spectrum.input import SingleHistInput
from spectrum.pipeline import TransformerBase
from spectrum.tools.feeddown import data_feeddown
from spectrum.broot import BROOT as br
from vault.datavault import DataVault


@pytest.fixture
def data():
    cyield = (
        (
            DataVault().input("data", histname="MassPtSM0"),
            data_feeddown(),
        ),
        (
            DataVault().input("single #pi^{0}", "low", "PhysEff"),
            DataVault().input("single #pi^{0}", "high", "PhysEff"),
        )
    )
    incnlo = DataVault().input("theory", "incnlo")
    return (cyield, incnlo)


class ErrorsTransformer(TransformerBase):
    def transform(self, data, loggs):
        for i in br.range(data):
            data.SetBinError(i, 0.0001)
        data.Sumw2()
        return data


def normalize(hist, loggs):
    hist.Scale(1. / hist.Integral(), "w")
    return hist


def theory_prediction():
    pipeline = Pipeline([
        ("raw", SingleHistInput("#sigma_{total}")),
        ("errors", ErrorsTransformer()),
        ("integral", FunctionTransformer(func=normalize)),
    ])
    return pipeline


def cyield(particle):
    options = CompositeCorrectedYieldOptions(particle=particle)
    return Pipeline([
        ("analysis", CorrectedYield(options)),
        ("integral", FunctionTransformer(func=normalize)),
    ])


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_simple(data):
    estimator = ComparePipeline([
        ("data", cyield(particle="#pi^{0}")),
        ("INCNLO", theory_prediction()),
    ], plot=True)

    with open_loggs() as loggs:
        estimator.transform(data, loggs=loggs)
