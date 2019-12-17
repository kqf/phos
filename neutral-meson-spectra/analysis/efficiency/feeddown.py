import ROOT
import pytest

import spectrum.broot as br
from spectrum.tools.feeddown import FeeddownEstimator, data_feeddown
from spectrum.options import FeeddownOptions
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
from spectrum.plotter import plot


def plot_func(data, loggs):
    func_feeddown = ROOT.TF1(
        "feeddown",
        "[2] * (1 + [0] * TMath::Exp(- x * x / [1] / [1] / 2))",
        0.8, 10
    )
    func_feeddown.SetTitle("Fit")
    func_feeddown.SetLineColor(ROOT.kBlack)
    func_feeddown.SetLineStyle(9)
    func_feeddown.SetParNames("A", "Sigma", "Scale")
    func_feeddown.FixParameter(0, 0.453)
    func_feeddown.FixParameter(1, 1.35)
    func_feeddown.FixParameter(2, 0.0478)
    data.Fit(func_feeddown, "RQ")
    data.SetTitle(
        "MC; p_{T} (GeV/#it{c});"
        "#frac{dN(#pi^{0} #leftarrow K_{0}^{s})}{dp_{T}} / "
        "#frac{dN(all)}{dp_{T}}"
    )
    plot(
        [data, func_feeddown],
        logy=False,
        csize=(156, 126),
        yoffset=1.75,
        oname="results/analysis/feeddown.pdf",

    )
    print()
    br.report(func_feeddown, limits=True)
    return data


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_feeddown_correction():
    options = FeeddownOptions(pt="config/pt-feeddown.json")
    options.plot_func = plot_func
    with open_loggs() as loggs:
        estimator = FeeddownEstimator(options)
        output = estimator.transform(data_feeddown(), loggs)
        Comparator().compare(output)
    assert output.GetEntries() > 0
