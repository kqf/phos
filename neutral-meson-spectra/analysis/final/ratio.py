import ROOT
import pytest

from spectrum.spectra import ratio
from spectrum.plotter import plot


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_ratio(pythia6_eta_pion_ratio, ptmin=5.5, ptmax=22):
    data = ratio()
    data.SetTitle("Data")

    ff = ROOT.TF1("ff", "[0]", ptmin, ptmax)
    ff.SetParameter(0, 0.5)
    data.Fit(ff, "RQ")
    print()
    print(r"\def \etaPionRatioValue {{{:.3g}}}".format(ff.GetParameter(0)))
    print(r"\def \etaPionRatioValueError {{{:.3g}}}".format(ff.GetParError(0)))
    print(r"\def \minEtaPionRatioFit {{{:.3g}}}".format(ptmin))
    print(r"\def \maxEtaPionRatioFit {{{:.3g}}}".format(ptmax))
    print(r"\def \etaPionRatioChi {{{:.3g}}}".format(
        ff.GetChisquare() / ff.GetNDF()
    ))
    ff.SetRange(2, 22)
    ff.SetLineColor(ROOT.kBlack)
    ff.SetLineStyle(7)
    ff.SetTitle("Constant fit")

    plot(
        [data, pythia6_eta_pion_ratio, ff],
        ytitle="#eta / #pi^{0}",
        xtitle="p_{T} (GeV/#it{c})",
        logy=False,
        logx=True,
        xlimits=(1.9, 22),
        ylimits=(0, 1.4),
        csize=(128, 96),
        legend_pos=(0.65, 0.7, 0.8, 0.88),
        yoffset=1.4,
        more_logs=True,
        oname="results/eta-pion-ratio.pdf"
    )
