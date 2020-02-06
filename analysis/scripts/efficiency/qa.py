import pytest

import ROOT
import spectrum.broot as br
import spectrum.plotter as plt

from spectrum.vault import DataVault
from spectrum.output import open_loggs
from spectrum.pipeline import SingleHistReader


@pytest.fixture
def spmc(particle, selection, histname):
    production = "single {}".format(particle)
    histname = histname.format(particle)
    return (
        DataVault().input(production, "low", selection, histname=histname),
        DataVault().input(production, "high", selection, histname=histname),
    )


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("target", ["eta_phi"])
@pytest.mark.parametrize("selection", ["PhysEff"])
@pytest.mark.parametrize("histname", ["hEtaPhi_#gamma"])
def test_eta_phi(particle, spmc, oname, stop):
    with plt.style(), plt.canvas(oname=oname, stop=stop):
        with open_loggs() as loggs:
            ROOT.gStyle.SetPalette(ROOT.kLightTemperature)
            ROOT.gPad.SetLogz(True)
            ROOT.gPad.SetRightMargin(0.12)
            summed = br.hsum([
                SingleHistReader().transform(d, loggs)
                for d in spmc
            ])
            summed.GetYaxis().SetTitle("#it{y}")
            summed.GetYaxis().SetTitleOffset(1.0)
            summed.GetYaxis().SetTitleFont(62)
            summed.GetXaxis().SetTitleFont(62)
            summed.Draw("colz")


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("selection, target", [
    ("NoWeights", "noweights"),
    ("PhysEff", "physeff"),
])
@pytest.mark.parametrize("histname", ["hPtLong_{}"])
def test_spectral_shape(particle, spmc, ltitle, selection, stop, oname):
    with open_loggs() as loggs:
        hists = []
        for name, d in zip(["low #it{p}_{T}", "high #it{p}_{T}"], spmc):
            hist = SingleHistReader().transform(d, loggs)
            hist.SetTitle(name)
            hists.append(br.hist2graph(hist, "positive"))

        plt.plot(
            hists,
            stop=stop,
            logx=True,
            xtitle="#it{p}_{T} (GeV/#it{c})",
            ytitle="#frac{d#it{N}}{d#it{p}_{T}} (GeV^{-1}#it{c})",
            xlimits=(0.8, 99),
            ltitle=ltitle,
            oname=oname,
            legend_pos=(0.7, 0.7, 0.85, 0.85),
            yoffset=1.4,
        )
