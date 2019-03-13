import pytest
from spectrum.comparator import Comparator
from vault.datavault import DataVault
from spectrum.pipeline import TransformerBase
from spectrum.pipeline import ComparePipeline
from spectrum.input import SingleHistInput


class EtaPionRatio(TransformerBase):
    def __init__(self, options, plot=False):
        super(EtaPionRatio, self).__init__()
        self.pipeline = ComparePipeline([
            ("#eta", SingleHistInput("hPtLong_#eta")),
            ("#pi^{0}", SingleHistInput("hPtLong_#pi^{0}")),
        ], plot)


@pytest.mark.onlylocal
def test_draw_generated_spectra():
    pi0 = DataVault().input("pythia8", "ep_ratio_3 LHC18")
    eta = DataVault().input("pythia8", "ep_ratio_3 LHC18")

    ratio = EtaPionRatio(None).transform((eta, pi0), {})
    Comparator().compare(ratio)
