import pytest

from spectrum.processing import DataSlicer
from spectrum.processing import MassFitter
from spectrum.output import open_loggs
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import Pipeline
from spectrum.processing import InvariantMassExtractor

from spectrum.options import Options
from vault.datavault import DataVault


class UpdatedAnalysis(TransformerBase):

    def __init__(self, options=Options()):
        super(UpdatedAnalysis, self).__init__()
        self.options = options
        self.pipeline = Pipeline([
            ('data_slicer', DataSlicer(self.options.pt)),
            ('mass_extractor', InvariantMassExtractor(self.options.invmass)),
            ('mass_fitter', MassFitter(self.options.invmass.use_mixed))
        ])


@pytest.fixture
def data():
    return DataVault().input("data", histname="MassPtSM0", label='Test')


@pytest.mark.onlylocal
@pytest.mark.parametrize("mixed", [True, False])
def test_analysis(data, mixed):
    options = Options()
    options.pt.use_mixed = mixed
    with open_loggs() as loggs:
        masses = UpdatedAnalysis(options).transform(data, loggs)
    assert len(masses) > 0
