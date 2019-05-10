import pytest
from spectrum.comparator import Comparator
from spectrum.input import SingleHistInput
from spectrum.pipeline import ComparePipeline
from spectrum.pipeline import TransformerBase
from vault.datavault import DataVault


@pytest.fixture
def data():
    return (
        DataVault().input("pythia8", "ep_ratio_3"),
        DataVault().input("pythia8", "ep_ratio_3"),
    )


class EtaPionRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(EtaPionRatio, self).__init__()
        self.pipeline = ComparePipeline([
            ("#eta", SingleHistInput("hPtLong_#eta")),
            ("#pi^{0}", SingleHistInput("hPtLong_#pi^{0}")),
        ], plot)


@pytest.mark.onlylocal
def test_calculate_eta_pion_ratio(data):
    ratio = EtaPionRatio(None).transform(data, {})
    Comparator().compare(ratio)
