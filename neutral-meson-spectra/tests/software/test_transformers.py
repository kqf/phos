import ROOT
import json
import pytest
import numpy as np
from math import exp
import array

from spectrum.pipeline import RebinTransformer
from spectrum.output import open_loggs
from spectrum.comparator import Comparator
from spectrum.broot import BROOT as br
from spectrum.input import SingleHistInput

from vault.datavault import DataVault


@pytest.fixture
def edges(etype):
    if etype == "normal":
        return np.linspace(0, 20, 2000)

    with open("config/pt.json") as f:
        data = json.load(f)
    return data["#pi^{0}"]["ptedges"]


@pytest.fixture
def edges_eta():
    with open("config/pt.json") as f:
        data = json.load(f)
    return data["#eta"]["ptedges"]


@pytest.mark.parametrize("func", [
    lambda i: 1,
    lambda i: exp(-i / 20.),
])
@pytest.mark.parametrize("etype", [
    "normal",
    "#pi^{0}",
])
def test_rebins_flat_data(edges, edges_eta, func):
    hist = ROOT.TH1F("hist", "test", len(edges) - 1, array.array('d', edges))
    hist.label = "original"
    for i in br.range(hist):
        hist.SetBinContent(i, func(i))
        hist.SetBinError(i, func(i) * 1e-2)

    hist.logy = True
    with open_loggs() as loggs:
        rebinned = RebinTransformer(True, edges).transform(hist, loggs)
        rebinned.label = "transformed"

    Comparator().compare(hist, rebinned)
    assert hist is not rebinned


@pytest.mark.skip()
@pytest.fixture
def pion_data():
    return (
        DataVault().input("single #pi^{0}", "low", "PhysEff"),
        DataVault().input("single #pi^{0}", "high", "PhysEff"),
    )


@pytest.mark.parametrize("etype", [
    "#pi^{0}",
])
def test_rebins_data(etype, edges, pion_data):
    for data in pion_data:
        histname = "hPt_#pi^{0}_primary_standard"
        with open_loggs() as loggs:
            hist = SingleHistInput(histname).transform(data, loggs)
            hist.label = "original"
            hist.logy = True

            rebinned = RebinTransformer(False, edges).transform(hist, loggs)
            rebinned.label = "transformed"
            rebinned.logy = True
            Comparator().compare(hist, rebinned)
