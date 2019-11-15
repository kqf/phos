from __future__ import print_function
import pytest

import ROOT
import spectrum.broot as br
from spectrum.options import ProbeTofOptions
from vault.datavault import DataVault
from spectrum.output import open_loggs
from spectrum.tools.probe import TagAndProbe
from spectrum.tools.validate import validate  # noqa
from spectrum.plotter import plot


@pytest.fixture
def data():
    return (
        DataVault().input("data", "staging tof", listname="TagAndProbleTOF",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", "staging tof", listname="TagAndProbleTOF",
                          histname="MassEnergyAll_SM0"),
    )


@pytest.fixture
def data_old():
    return (
        DataVault().input("data", "uncorrected",
                          "TagAndProbleTOFOnlyTender",
                          histname="MassEnergyTOF_SM0"),
        DataVault().input("data", "uncorrected",
                          "TagAndProbleTOFOnlyTender",
                          histname="MassEnergyAll_SM0"),
    )


@pytest.fixture
def fitfunc():
    tof_eff = ROOT.TF1(
        "tof",
        "1 - [2] / (1 + TMath::Exp(x * [0] + [1]))"
        " - [3] * TMath::Exp(x * [4])", 0, 20
    )
    tof_eff.SetTitle("Fit")
    tof_eff.SetLineColor(ROOT.kBlack)
    tof_eff.SetLineStyle(9)
    tof_eff.SetParNames(*["A", "B", "C", "D"])

    tof_eff.SetParameter(0, -1.02802e+00)
    tof_eff.SetParameter(1, 8.51857e+00)
    tof_eff.SetParameter(2, 6.19420e-01)
    tof_eff.SetParameter(3, 1.30498e+00)
    tof_eff.SetParameter(4, -1.78716e+00)
    return tof_eff


@pytest.fixture
def efficiency(data):
    with open_loggs() as loggs:
        probe_estimator = TagAndProbe(ProbeTofOptions(), False)
        efficiency = probe_estimator.transform(data, loggs)
    return efficiency


@pytest.fixture
def oname():
    return "results/analysis/data/tof.pdf"


@pytest.mark.thesis
@pytest.mark.onlylocal
@pytest.mark.interactive
def test_estimate_tof_efficiency(efficiency, oname, fitfunc):
    bins = br.edges(efficiency)
    fitfunc.SetRange(min(bins), max(bins))
    efficiency.Fit(fitfunc, "RWW")
    br.report(fitfunc)
    plot(
        [efficiency, fitfunc],
        logy=False,
        csize=(126, 126),
        legend_pos=(0.20, 0.7, 0.35, 0.85),
        ltitle="#pi^{0} #rightarrow #gamma #gamma",
        oname=oname
    )
    # validate(br.hist2dict(efficiency), "efficiency_tag")
