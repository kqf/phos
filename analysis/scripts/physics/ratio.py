import ROOT
import pytest

import spectrum.broot as br
from spectrum.spectra import ratio
from spectrum.plotter import plot


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target", ["eta-pion-ratio"])
def test_ratio(pythia6_eta_pion_ratio, coname, ptmin=4.5, ptmax=22):
    data = ratio()
    data.SetTitle("Data")

    ff = ROOT.TF1("etaPionRatio", "[0]", ptmin, ptmax)
    ff.SetParameter(0, 0.5)
    ff.SetParName(0, "Value")
    data.Fit(ff, "RQ")

    br.report(ff, limits=True)
    ff.SetRange(2, 22)
    ff.SetLineColor(ROOT.kBlack)
    ff.SetLineStyle(7)
    ff.SetTitle("Constant fit")

    pythia6 = br.hist2graph(pythia6_eta_pion_ratio)
    pythia6.SetTitle("PYTHIA 6")
    plot(
        [data, pythia6, ff],
        ytitle="#eta / #pi^{0}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        logy=False,
        logx=True,
        xlimits=(1.9, 22),
        ylimits=(0, 1.4),
        csize=(96, 96 * 0.64),
        tmargin=0.01,
        rmargin=0.01,
        lmargin=0.1,
        yoffset=1.,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        more_logs=True,
        options=["p", "lx"],
        oname=coname.format(""),
    )
