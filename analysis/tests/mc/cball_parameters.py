import pytest

from spectrum.analysis import Analysis
from spectrum.comparator import Comparator
from spectrum.options import Options
from spectrum.output import open_loggs
from spectrum.pipeline import Pipeline
from spectrum.processing import DataPreparator, MassFitter
from spectrum.vault import DataVault


class MassExtractor(object):

    def __init__(self, options=Options()):
        super(MassExtractor, self).__init__()
        self.options = options
        self._loggs = None

    def transform(self, inputs, loggs):
        pipeline = Pipeline([
            ("input", inputs),
            ("slice", DataPreparator(self.options.pt)),
            ("fitmasses", MassFitter(self.options.invmass)),
        ])

        output = pipeline.transform(None, loggs)
        return output


@pytest.fixture
def data():
    return DataVault().input("single #pi^{0}", "high", listname="PhysEff")


@pytest.onlylocal
@pytest.interactive
def test_background_fitting(data):
    with open_loggs("fixed cb parameters") as loggs:
        options = Options()
        outputs1 = Analysis(options).transform(data, loggs)

    with open_loggs("relaxed cb parameters") as loggs:
        options = Options()
        options.signal.relaxed = True
        outputs2 = Analysis(options).transform(data, loggs)

    diff = Comparator()
    for parameter in zip(outputs1, outputs2):
        diff.compare(*parameter)
