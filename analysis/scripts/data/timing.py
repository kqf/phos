import ROOT
import pytest
from repoze.lru import lru_cache

from spectrum.pipeline import SingleHistReader
from spectrum.output import open_loggs
from spectrum.vault import DataVault

import spectrum.plotter as plt


@pytest.fixture
def oname(module_number):
    pattern = "images/analysis/timing/EnergyVsTimingSM{}.pdf"
    return pattern.format(module_number)


@pytest.fixture
def data(module_number):
    return DataVault().input(
        "data", "timing plots",
        histname="hClusterEvsTM{}".format(module_number)
    )


@lru_cache(maxsize=1024)
def draw_text(text, coordinates=(0.58, 0.75, 0.78, 0.88)):
    x1, y1, x2, y2 = coordinates
    pave = ROOT.TPaveText(x1, y1, x2, y2, "NDC")
    pave.AddText(text)
    pave.SetMargin(0)
    pave.SetBorderSize(0)
    pave.SetFillStyle(0)
    pave.SetTextAlign(13)
    pave.SetTextFont(42)
    pave.Draw("same")
    return pave


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("module_number", list(range(1, 5)))
def test_eta_phi(data, module_number, oname, stop):
    with plt.style(), plt.canvas(oname=oname, stop=stop):
        with open_loggs() as loggs:
            ROOT.gStyle.SetPalette(ROOT.kLightTemperature)
            ROOT.gPad.SetLogz(True)
            ROOT.gPad.SetRightMargin(0.12)
            hist = SingleHistReader().transform(data, loggs)
            hist.GetYaxis().SetTitleOffset(1.5)
            hist.GetYaxis().SetTitle("cluster timing (seconds)")
            hist.GetXaxis().SetTitle("cluster energy (GeV)")
            hist.GetYaxis().SetTitleFont(62)
            hist.GetXaxis().SetTitleFont(62)
            hist.Draw("colz")
            draw_text("Module {}".format(module_number))
