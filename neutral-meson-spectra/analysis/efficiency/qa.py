import pytest

import ROOT
from spectrum.input import SingleHistInput
from spectrum.output import open_loggs
import spectrum.broot as br  # noqa
from spectrum.comparator import Comparator  # noqa

import spectrum.plotter as plt
from spectrum.tools.validate import validate  # noqa
from vault.datavault import DataVault


@pytest.fixture
def data(particle):
    production = "single {}".format(particle)
    return {
        "low p_{T}": DataVault().input(production, "low", "PhysEff"),
        "high p_{T}": DataVault().input(production, "high", "PhysEff"),
    }


@pytest.fixture
def oname(particle):
    return "results/analysis/spmc/eta_phi_{}.pdf".format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_eta_phi(particle, data, oname):
    with plt.style(), plt.pcanvas(oname=oname), open_loggs() as loggs:
        ROOT.gStyle.SetPalette(ROOT.kLightTemperature)
        ROOT.gPad.SetLogz(True)
        summed = br.hsum([
            SingleHistInput("hEtaPhi_#gamma").transform(d, loggs)
            for d in data.values()
        ])
        summed.Draw("colz")


@pytest.fixture
def ltitle(particle):
    return "{} #rightarrow #gamma#gamma".format(particle)


@pytest.fixture
def wname(particle):
    return "results/analysis/spmc/weighted_{}.pdf".format(br.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_spectral_shape(particle, data, ltitle, wname):
    with open_loggs() as loggs:
        hists = []
        for name, d in data.items():
            hist = SingleHistInput(
                "hPtLong_{}".format(particle)).transform(d, loggs)
            contents, errors, centers = br.bins(hist)
            idx = contents > 0
            graph = br.graph(name, centers[idx], contents[idx], dy=errors[idx])
            hists.append(graph)

        plt.plot(
            hists,
            logx=True,
            xtitle="p_{T}, (GeV/#it{c})",
            ytitle="#frac{dN}{dp_{T}} (GeV/#it{c})^{-1} ",
            xlimits=(0.3, 100),
            ltitle=ltitle,
            oname=wname,
            legend_pos=(0.7, 0.7, 0.85, 0.85),
            yoffset=1.4,
        )
