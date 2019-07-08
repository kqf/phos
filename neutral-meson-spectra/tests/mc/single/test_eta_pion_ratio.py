import pytest
from spectrum.comparator import Comparator
from spectrum.input import SingleHistInput
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import TransformerBase
from spectrum.output import open_loggs
from vault.datavault import DataVault


@pytest.fixture
def data():
    production = "single #pi^{0} debug 2"
    return (
        DataVault().input(production, "high", listname="PhysEff"),
        DataVault().input(production, "high", listname="PhysEff"),
    )


class EtaPionRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(EtaPionRatio, self).__init__()
        self.pipeline = ComparePipeline([
            ("#eta", SingleHistInput("hPtLong_#eta")),
            ("#pi^{0}", SingleHistInput("hPtLong_#pi^{0}")),
        ], plot)


@pytest.mark.onlylocal
@pytest.mark.interactive
def test_calculate_eta_pion_ratio(data):
    with open_loggs("eta pion ratio generated") as loggs:
        ratio = EtaPionRatio(None).transform(data, loggs)
        Comparator().compare(ratio)
