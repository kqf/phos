import ROOT
import pytest

import spectrum.broot as br
from spectrum.spectra import ratio
from spectrum.plotter import plot


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_ratio(pythia6_eta_pion_ratio, ptmin=4.5, ptmax=22):
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

    plot(
        [data, pythia6_eta_pion_ratio, ff],
        ytitle="#eta / #pi^{0}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        logy=False,
        logx=True,
        xlimits=(1.9, 22),
        ylimits=(0, 1.4),
        csize=(128, 96),
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        # yoffset=1.4,
        more_logs=True,
        oname="results/discussion/eta-pion-ratio.pdf"
    )
