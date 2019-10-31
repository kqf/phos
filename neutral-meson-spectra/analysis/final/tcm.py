import ROOT
import pytest  # noqa

import spectrum.sutils as su
from spectrum.spectra import spectrum
from spectrum.constants import mass
from spectrum.plotter import plot
from spectrum.constants import invariant_cross_section_code
from vault.formulas import FVault


@pytest.fixture
def tsallis(particle):
    tsallis = FVault().tf1("tsallis")
    tsallis.SetTitle("Tsallis fit")
    # tsallis.SetLineColor(ROOT.kBlue + 1)
    tsallis.SetNpx(1000)
    tsallis.SetLineColor(ROOT.kBlack)
    tsallis.SetLineStyle(7)

    if particle == "#pi^{0}":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.125)
        tsallis.SetParLimits(1, 0.100, 0.300)
        tsallis.FixParameter(2, 6.500)
        tsallis.SetParLimits(2, 6.000, 8.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(1.4, 20)

    if particle == "#eta":
        tsallis.SetParameter(0, 1)
        tsallis.SetParameter(1, 0.238)
        tsallis.SetParLimits(1, 0.200, 0.300)
        tsallis.SetParameter(2, 6.19)
        tsallis.SetParLimits(2, 5.5, 7.000)
        tsallis.FixParameter(3, mass(particle))
        tsallis.SetRange(2.2, 20)

    tsallis.FixParameter(3, mass(particle))
    tsallis.FixParameter(4, mass(particle))
    return tsallis


@pytest.fixture
def tcm(particle):
    tcm = FVault().tf1("tcm", "{} 13 TeV".format(particle))
    tcm.SetTitle("TCM fit")
    tcm.SetNpx(100)
    tcm.SetLineColor(ROOT.kBlack)
    tcm.SetLineWidth(2)

    if particle == "#pi^{0}":
        tcm.SetRange(0.7, 22)
        tcm.SetParameter(0, 0.1)
        tcm.SetParameter(1, 1.73e-01)
        tcm.SetParLimits(1, 0.1, 0.3)
        tcm.SetParameter(2, 0.1)
        tcm.SetParameter(3, 0.601)
        tcm.SetParLimits(3, 0.4, 1.0)
        tcm.SetParameter(4, 3.09)
        tcm.SetParLimits(4, 2.0, 4.0)

    if particle == "#eta":
        # pass
        tcm.SetParameter(0, 0.1)
        tcm.SetParLimits(0, 0, 1e4)
        tcm.SetParameter(1, 1.71e-01)
        tcm.SetParLimits(1, 0.1, 0.3)
        tcm.SetParameter(2, 0.1)
        tcm.SetParameter(3, 0.801)
        # tcm.SetParLimits(3, 0.7, 0.9)
        tcm.SetParameter(4, 3.059)
        # tcm.SetParLimits(4, 2.0, 4.0)

    tcm.FixParameter(5, mass(particle))
    return tcm


@pytest.fixture
def oname(particle):
    return "results/{{}}/{{}}_{}.pdf".format(su.spell(particle))


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("particle", [
    "#pi^{0}",
    "#eta",
])
def test_tcm_fit(particle, tcm, tsallis, oname):
    cs = spectrum(particle)
    cs.SetTitle("Data")
    cs.Fit(tcm, "R")
    cs.Fit(tsallis, "R")
    plot(
        [cs, tcm, tsallis],
        ytitle=invariant_cross_section_code(),
        xtitle="p_{T} (GeV/#it{c})",
        # xlimits=(0.7, 22),
        csize=(96, 128),
        ltitle="{} #rightarrow #gamma#gamma".format(particle),
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=False,
        oname=oname.format("phenomenology", "fits"),
    )
