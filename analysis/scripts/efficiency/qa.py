import pytest

import ROOT
from spectrum.pipeline import SingleHistReader
from spectrum.output import open_loggs
import spectrum.broot as br  # noqa
from spectrum.comparator import Comparator  # noqa

import spectrum.plotter as plt
from spectrum.tools.validate import validate  # noqa
from spectrum.vault import DataVault


@pytest.fixture
def spmc(particle, selection, histname):
    production = "single {}".format(particle)
    histname = histname.format(particle)
    return (
        DataVault().input(production, "low", selection, histname=histname),
        DataVault().input(production, "high", selection, histname=histname),
    )


@pytest.fixture
def oname(particle):
    return "results/analysis/spmc/eta_phi_{}.pdf".format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("selection", ["PhysEff"])
@pytest.mark.parametrize("histname", ["hEtaPhi_#gamma"])
def test_eta_phi(particle, spmc, oname):
    with plt.style(), plt.pcanvas(oname=oname), open_loggs() as loggs:
        ROOT.gStyle.SetPalette(ROOT.kLightTemperature)
        ROOT.gPad.SetLogz(True)
        ROOT.gPad.SetRightMargin(0.12)
        summed = br.hsum([
            SingleHistReader().transform(d, loggs)
            for d in spmc
        ])
        summed.GetYaxis().SetTitleOffset(1.0)
        summed.GetYaxis().SetTitleFont(62)
        summed.GetXaxis().SetTitleFont(62)
        summed.Draw("colz")


@pytest.fixture
def wname(particle, selection):
    pattern = "results/analysis/spmc/{}_{}.pdf"
    return pattern.format(selection.lower(), br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
@pytest.mark.parametrize("selection", [
    "NoWeights",
    "PhysEff",
])
@pytest.mark.parametrize("histname", ["hPtLong_{}"])
def test_spectral_shape(particle, spmc, ltitle, selection, wname):
    with open_loggs() as loggs:
        hists = []
        for name, d in zip(["low p_{T}", "high p_{T}"], spmc):
            hist = SingleHistReader().transform(d, loggs)
            hist.SetTitle(name)
            hists.append(br.hist2graph(hist, "positive"))

        plt.plot(
            hists,
            logx=True,
            xtitle="p_{T} (GeV/#it{c})",
            ytitle="#frac{dN}{dp_{T}} (GeV/#it{c})^{-1} ",
            xlimits=(0.8, 100),
            ltitle=ltitle,
            oname=wname,
            legend_pos=(0.7, 0.7, 0.85, 0.85),
            yoffset=1.4,
        )