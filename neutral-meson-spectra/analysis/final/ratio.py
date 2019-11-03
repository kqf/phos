import ROOT
import pytest

from spectrum.spectra import ratio
from spectrum.plotter import plot


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_ratio(pythia6_eta_pion_ratio):
    data = ratio()
    data.SetTitle("Data")

    constant = ROOT.TF1("constant", "[0]", 5.5, 22)
    constant.SetParameter(0, 0.5)
    data.Fit(constant, "RQ")
    constant.SetRange(2, 22)
    constant.SetLineColor(ROOT.kBlack)
    constant.SetLineStyle(7)
    constant.SetTitle("Constant fit")

    plot(
        [data, pythia6_eta_pion_ratio, constant],
        ytitle="#eta / #pi^{0}",
        xtitle="p_{T} (GeV/#it{c})",
        logy=False,
        logx=True,
        xlimits=(1.9, 22),
        ylimits=(0, 1.4),
        csize=(128, 96),
        # legend_pos=(0.65, 0.7, 0.8, 0.88),
        legend_pos=(0.52, 0.72, 0.78, 0.88),
        yoffset=1.4,
        more_logs=True,
        oname="results/pythia/etapion.pdf"
    )
