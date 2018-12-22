import pytest
import ROOT

from spectrum.broot import BROOT as br


@pytest.fixture()
def ratio():
    ratio = ROOT.TH1F("test", "test", 30, 0, 20)
    for i in br.range(ratio):
        ratio.SetBinContent(i, 1)
    ratio.SetBinContent(30, 1)

    ratio.SetBinContent(15, 1.5)
    ratio.SetBinContent(14, -1.3)
    return ratio


@pytest.mark.skip("fix root_numpy")
def test_interface(ratio):
    from tools.deviation import MaxDeviation
    output = MaxDeviation().transform(ratio, "test")
    assert output.GetParameter(0) == 1.5 - 1.
