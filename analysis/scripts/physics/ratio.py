import ROOT
import pytest

import spectrum.broot as br
import spectrum.plotter as plt
from spectrum.spectra import ratio


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
@pytest.mark.parametrize("target", ["eta-pion-ratio"])
def test_ratio(pythia6_eta_pion_ratio, eta_pion_ratio_fitf, coname):
    data = ratio()
    data.SetTitle("Data")
    data.Fit(eta_pion_ratio_fitf, "RQ")
    br.report(eta_pion_ratio_fitf, limits=True)

    eta_pion_ratio_fitf.SetRange(2, 22)
    eta_pion_ratio_fitf.SetLineColor(ROOT.kBlack)
    eta_pion_ratio_fitf.SetLineStyle(7)
    eta_pion_ratio_fitf.SetTitle("Constant fit")

    pythia6 = br.hist2graph(pythia6_eta_pion_ratio)
    pythia6.SetTitle("PYTHIA 6")
    plt.plot(
        [data, pythia6, eta_pion_ratio_fitf],
        ytitle="#eta / #pi^{0}",
        xtitle="#it{p}_{T} (GeV/#it{c})",
        logy=False,
        logx=True,
        xlimits=(1.9, 22),
        ylimits=(0, 1.4),
        csize=(129, 96),
        tmargin=0.01,
        rmargin=0.01,
        lmargin=0.1,
        yoffset=1.,
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        more_logs=True,
        options=["p", "lx", "l"],
        oname=coname.format(""),
    )
